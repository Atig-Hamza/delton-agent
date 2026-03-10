"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Video Rendering Engine                 ║
║                                                  ║
║  Orchestrates all skills to produce MP4 output   ║
╚══════════════════════════════════════════════════╝
"""

import os
import time
import numpy as np
from PIL import Image

from engine.timeline import Timeline
from engine.asset_manager import AssetManager
from engine.exporter import Exporter
from skills.color_grading import ColorGrader
from skills.transitions import TransitionEngine
from skills.motion_graphics import MotionGraphicsEngine
from skills.vfx import VFXEngine
from skills.speed_effects import SpeedEffects
from skills.montage_planner import MontagePlanner
from config import OUTPUT_DIR, DEFAULT_FPS


class DeltonRenderer:
    """
    Main rendering engine.  Converts an AI-generated montage plan dict
    into a real MP4 video file.

    Usage:
        renderer = DeltonRenderer()
        renderer.load_plan(plan_dict)
        output_path = renderer.render()
    """

    def __init__(self):
        self.plan: dict = None
        self.timeline = Timeline()
        self.asset_manager = AssetManager()
        self.exporter = Exporter()
        self.color_grader = ColorGrader()
        self.transition_engine = TransitionEngine()
        self.motion_graphics = MotionGraphicsEngine(asset_manager=self.asset_manager)
        self.vfx_engine = VFXEngine()
        self.speed_effects = SpeedEffects()
        self.planner = MontagePlanner()

    # ─── Public API ───────────────────────────────────────
    def load_plan(self, plan: dict):
        """Load and normalise a montage plan."""
        self.plan = self.planner.prepare(dict(plan))
        self.timeline.build_from_plan(self.plan)

    def render(self) -> str:
        """
        Render the loaded plan to an MP4 file.

        Returns:
            str: Absolute path to the output video.
        Raises:
            RuntimeError: If no plan is loaded.
        """
        if not self.plan:
            raise RuntimeError("No plan loaded. Call load_plan() first.")

        from moviepy.editor import concatenate_videoclips, VideoClip

        resolution = tuple(self.plan.get("resolution", [1920, 1080]))
        fps = self.plan.get("fps", DEFAULT_FPS)
        scenes = self.plan.get("scenes", [])
        color_grade = self.plan.get("color_grade")
        global_fx = self.plan.get("global_effects", {})

        # ── Render each scene to a clip ──
        scene_clips = []
        for scene in scenes:
            clip = self._render_scene(scene, resolution, fps)
            scene_clips.append(clip)

        if not scene_clips:
            raise RuntimeError("Plan produced no renderable scenes.")

        # ── Concatenate ──
        final_clip = concatenate_videoclips(scene_clips, method="compose")

        # ── Global color grade ──
        if color_grade:
            final_clip = self._apply_grade(final_clip, color_grade)

        # ── Global effects (vignette, film grain, letterbox) ──
        if global_fx.get("vignette"):
            final_clip = self._apply_global_vfx(final_clip, "vignette")
        if global_fx.get("film_grain"):
            final_clip = self._apply_global_vfx(final_clip, "film_grain")
        if global_fx.get("letterbox"):
            final_clip = self._apply_letterbox(final_clip, resolution,
                                                global_fx.get("letterbox_ratio", 2.35))

        # ── Export ──
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        export_cfg = self.plan.get("export", {})
        fmt = export_cfg.get("format", "mp4")
        project_name = self.plan.get("project_name", "delton_output")
        output_path = self.exporter.get_output_path(project_name, fmt, OUTPUT_DIR)

        self.exporter.export(
            final_clip,
            output_path,
            {**export_cfg, "fps": fps},
        )
        return output_path

    # ─── Scene rendering ──────────────────────────────────
    def _render_scene(self, scene: dict, resolution: tuple, fps: int):
        """
        Convert one scene dict to a MoviePy VideoClip.
        The clip is assembled from:
          1. A pre-computed background numpy array
          2. Per-frame animated element overlays
          3. Per-frame VFX
        """
        from moviepy.editor import VideoClip

        duration = max(float(scene.get("duration", 3.0)), 0.1)
        elements = scene.get("elements", [])
        background = scene.get("background", {})
        vfx_list = scene.get("vfx", [])
        speed_effect = scene.get("speed_effect", "normal")
        speed_value = float(scene.get("speed_value", 1.0))

        width, height = resolution

        # Pre-compute static background
        bg_array = np.array(self._create_background(background, width, height))

        def make_frame(t):
            # Copy background
            img = Image.fromarray(bg_array.copy())

            # Render animated elements
            for element in elements:
                try:
                    img = self.motion_graphics.render_element(img, element, t, duration)
                except Exception:
                    pass  # never let a single element crash the whole render

            # Apply VFX
            for effect in vfx_list:
                try:
                    img = self.vfx_engine.apply(img, effect, t, duration)
                except Exception:
                    pass

            return np.array(img.convert("RGB"))

        clip = VideoClip(make_frame, duration=duration)
        clip = clip.set_fps(fps)

        # Apply speed effects
        if speed_effect != "normal":
            clip = self.speed_effects.apply(clip, speed_effect, speed_value)

        return clip

    # ─── Background creation ──────────────────────────────
    def _create_background(self, background: dict, width: int, height: int) -> Image.Image:
        bg_type = background.get("type", "solid")

        if bg_type == "gradient":
            return self._create_gradient(
                width, height,
                background.get("gradient_start", [0, 0, 0]),
                background.get("gradient_end", [30, 30, 60]),
                background.get("gradient_direction", "vertical"),
            )

        # Solid (default) — also handles unknown types gracefully
        color = background.get("color", [10, 10, 20])
        if not color or not isinstance(color, (list, tuple)) or len(color) < 3:
            color = [10, 10, 20]
        return Image.new("RGB", (width, height), tuple(int(c) for c in color[:3]))

    def _create_gradient(self, width, height,
                         start_color, end_color, direction) -> Image.Image:
        """Fast numpy-based gradient background."""
        s = np.array(start_color[:3], dtype=np.float32)
        e = np.array(end_color[:3],   dtype=np.float32)

        if direction == "vertical":
            t = np.linspace(0, 1, height, dtype=np.float32)[:, None, None]
            arr = np.broadcast_to(s + (e - s) * t, (height, width, 3)).copy()

        elif direction == "horizontal":
            t = np.linspace(0, 1, width, dtype=np.float32)[None, :, None]
            arr = np.broadcast_to(s + (e - s) * t, (height, width, 3)).copy()

        elif direction == "diagonal":
            ty = np.linspace(0, 1, height, dtype=np.float32)[:, None]
            tx = np.linspace(0, 1, width,  dtype=np.float32)[None, :]
            t  = ((ty + tx) / 2)[..., None]
            arr = s + (e - s) * t

        else:  # radial
            cx, cy = width / 2, height / 2
            y_idx, x_idx = np.ogrid[:height, :width]
            max_d = np.hypot(cx, cy)
            t = np.clip(np.hypot(x_idx - cx, y_idx - cy) / max_d, 0, 1)[..., None]
            arr = s + (e - s) * t

        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    # ─── Global post-processing ───────────────────────────
    def _apply_grade(self, clip, grade_name: str):
        """Apply color grading to every frame of the clip."""
        def grade_frame(get_frame, t):
            return self.color_grader.apply_to_frame(get_frame(t), grade_name)
        return clip.fl(grade_frame)

    def _apply_global_vfx(self, clip, effect: str):
        """Wrap a clip with a full-frame VFX."""
        def apply_fx(get_frame, t):
            frame = get_frame(t)
            img = Image.fromarray(frame.astype(np.uint8))
            img = self.vfx_engine.apply(img, effect, t, clip.duration)
            return np.array(img.convert("RGB"))
        return clip.fl(apply_fx)

    def _apply_letterbox(self, clip, resolution: tuple, ratio: float):
        """Add black letterbox bars for cinematic aspect ratio."""
        width, height = resolution
        target_height = int(width / ratio)
        bar_h = max(0, (height - target_height) // 2)
        if bar_h == 0:
            return clip

        def add_bars(get_frame, t):
            frame = get_frame(t).copy()
            frame[:bar_h, :] = 0
            frame[height - bar_h:, :] = 0
            return frame

        return clip.fl(add_bars)
