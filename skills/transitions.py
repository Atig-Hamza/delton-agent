"""
╔══════════════════════════════════════════════════╗
║  Skill 03: Premium Transitions                   ║
╚══════════════════════════════════════════════════╝
"""

import numpy as np


class TransitionEngine:
    """
    Applies transitions between MoviePy clips.
    Each transition takes (clip1, clip2, duration) and returns a single blended clip.
    """

    def apply(self, clip1, clip2, transition_name: str, duration: float = 0.5):
        """Apply a named transition between two clips."""
        handler = getattr(self, f"_t_{transition_name}", self._t_crossfade)
        try:
            return handler(clip1, clip2, duration)
        except Exception:
            return self._t_crossfade(clip1, clip2, duration)

    # ─── Crossfade ────────────────────────────────────
    def _t_crossfade(self, clip1, clip2, duration):
        from moviepy.editor import CompositeVideoClip
        c1 = clip1
        c2 = clip2.set_start(clip1.duration - duration)
        c1 = c1.crossfadeout(duration)
        c2 = c2.crossfadein(duration)
        return CompositeVideoClip([c1, c2]).set_duration(clip1.duration + clip2.duration - duration)

    def _t_fade(self, clip1, clip2, duration):
        from moviepy.editor import concatenate_videoclips
        c1 = clip1.fadeout(duration)
        c2 = clip2.fadein(duration)
        return concatenate_videoclips([c1, c2])

    def _t_dissolve(self, clip1, clip2, duration):
        return self._t_crossfade(clip1, clip2, duration)

    def _t_flash_white(self, clip1, clip2, duration):
        from moviepy.editor import ImageClip, concatenate_videoclips
        w, h = clip1.size
        flash = ImageClip(np.full((h, w, 3), 255, dtype=np.uint8)).set_duration(duration / 2)
        c1 = clip1.fadeout(duration / 4)
        c2 = clip2.fadein(duration / 4)
        return concatenate_videoclips([c1, flash, c2])

    def _t_flash_black(self, clip1, clip2, duration):
        from moviepy.editor import ImageClip, concatenate_videoclips
        w, h = clip1.size
        flash = ImageClip(np.zeros((h, w, 3), dtype=np.uint8)).set_duration(duration / 2)
        c1 = clip1.fadeout(duration / 4)
        c2 = clip2.fadein(duration / 4)
        return concatenate_videoclips([c1, flash, c2])

    def _t_zoom_in(self, clip1, clip2, duration):
        from moviepy.editor import concatenate_videoclips
        from moviepy.video.fx.all import resize
        c1 = clip1.fl(lambda gf, t: self._zoom_frame(gf(t), 1 + 0.3 * (t / clip1.duration)))
        return concatenate_videoclips([c1, clip2])

    def _t_zoom_out(self, clip1, clip2, duration):
        from moviepy.editor import concatenate_videoclips
        c2 = clip2.fl(lambda gf, t: self._zoom_frame(gf(t), 1.3 - 0.3 * (t / max(clip2.duration, 0.01))))
        return concatenate_videoclips([clip1, c2])

    def _t_spin(self, clip1, clip2, duration):
        from moviepy.editor import concatenate_videoclips
        from PIL import Image
        import math

        def spin_end(gf, t):
            frame = gf(t)
            angle = 360 * (t / max(clip1.duration, 0.01))
            img = Image.fromarray(frame).rotate(angle, expand=False)
            return np.array(img)

        c1 = clip1.fl(spin_end)
        return concatenate_videoclips([c1, clip2])

    def _t_wipe_left(self, clip1, clip2, duration):
        return self._wipe(clip1, clip2, duration, direction="left")

    def _t_wipe_right(self, clip1, clip2, duration):
        return self._wipe(clip1, clip2, duration, direction="right")

    def _t_wipe_up(self, clip1, clip2, duration):
        return self._wipe(clip1, clip2, duration, direction="up")

    def _t_wipe_down(self, clip1, clip2, duration):
        return self._wipe(clip1, clip2, duration, direction="down")

    def _wipe(self, clip1, clip2, duration, direction="left"):
        from moviepy.editor import CompositeVideoClip, VideoClip
        from moviepy.video.VideoClip import VideoClip as VC

        total = clip1.duration + clip2.duration - duration
        w, h = clip1.size

        def make_frame(t):
            progress = max(0, min(1, (t - (clip1.duration - duration)) / duration))
            f1 = clip1.get_frame(min(t, clip1.duration - 1 / 30))
            f2 = clip2.get_frame(max(0, t - (clip1.duration - duration)))
            out = f1.copy()
            if direction == "left":
                cut = int(w * progress)
                out[:, :cut] = f2[:, :cut]
            elif direction == "right":
                cut = int(w * (1 - progress))
                out[:, cut:] = f2[:, cut:]
            elif direction == "up":
                cut = int(h * progress)
                out[:cut, :] = f2[:cut, :]
            elif direction == "down":
                cut = int(h * (1 - progress))
                out[cut:, :] = f2[cut:, :]
            return out

        return VC(make_frame, duration=total).set_fps(clip1.fps or 30)

    # ─── Helpers ──────────────────────────────────────
    @staticmethod
    def _zoom_frame(frame, zoom):
        from PIL import Image
        h, w = frame.shape[:2]
        img = Image.fromarray(frame)
        new_w, new_h = int(w * zoom), int(h * zoom)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        cropped = resized.crop((left, top, left + w, top + h))
        return np.array(cropped)

    # Aliases for names the AI may return
    _t_luma_fade = _t_crossfade
    _t_film_burn = _t_flash_white
    _t_pixelate = _t_crossfade
    _t_blur_transition = _t_crossfade
    _t_glitch = _t_flash_black
    _t_rgb_split = _t_flash_black
    _t_light_leak = _t_flash_white
    _t_whip_pan_left = _t_wipe_left
    _t_whip_pan_right = _t_wipe_right
    _t_whip_pan_up = _t_wipe_up
    _t_whip_pan_down = _t_wipe_down
    _t_circle_reveal = _t_crossfade
    _t_diamond_reveal = _t_crossfade
    _t_slice_horizontal = _t_wipe_up
    _t_slice_vertical = _t_wipe_left
