"""
╔══════════════════════════════════════════════════╗
║  Skill 04: Color Grading                         ║
╚══════════════════════════════════════════════════╝
"""

import numpy as np
from PIL import Image
from config import COLOR_GRADES


class ColorGrader:
    """Applies cinematic color grades to frames and MoviePy clips."""

    def apply_to_frame(self, frame: np.ndarray, grade_name: str) -> np.ndarray:
        """Apply a color grade to a numpy RGB frame (H×W×3, uint8)."""
        grade = COLOR_GRADES.get(grade_name)
        if grade is None:
            return frame

        frame = frame.astype(np.float32)

        # Contrast
        contrast = grade.get("contrast", 1.0)
        frame = (frame - 128) * contrast + 128

        # Saturation
        saturation = grade.get("saturation", 1.0)
        gray = 0.299 * frame[..., 0] + 0.587 * frame[..., 1] + 0.114 * frame[..., 2]
        gray = gray[..., np.newaxis]
        frame = gray + saturation * (frame - gray)

        # Shadows / Midtones / Highlights tinting
        shadows = np.array(grade.get("shadows", [0, 0, 0]), dtype=np.float32)
        highlights = np.array(grade.get("highlights", [255, 255, 255]), dtype=np.float32)

        # Luminance mask
        lum = (frame[..., 0] * 0.299 + frame[..., 1] * 0.587 + frame[..., 2] * 0.114)
        shadow_mask = np.clip(1.0 - lum / 255.0, 0, 1)[..., np.newaxis]
        highlight_mask = np.clip(lum / 255.0, 0, 1)[..., np.newaxis]

        frame += shadow_mask * (shadows - 128) * 0.15
        frame += highlight_mask * (highlights - 128) * 0.15

        return np.clip(frame, 0, 255).astype(np.uint8)

    def apply_to_image(self, img: Image.Image, grade_name: str) -> Image.Image:
        """Apply a color grade to a PIL Image."""
        arr = np.array(img.convert("RGB"))
        graded = self.apply_to_frame(arr, grade_name)
        result = Image.fromarray(graded)
        # Preserve alpha if present
        if img.mode == "RGBA":
            r, g, b = result.split()
            _, _, _, a = img.split()
            result = Image.merge("RGBA", (r, g, b, a))
        return result

    def apply_to_clip(self, clip, grade_name: str):
        """Wrap a MoviePy clip with per-frame color grading."""
        if grade_name not in COLOR_GRADES:
            return clip

        def grade_frame(get_frame, t):
            frame = get_frame(t)
            return self.apply_to_frame(frame, grade_name)

        return clip.fl(grade_frame, apply_to=["mask", "video"])
