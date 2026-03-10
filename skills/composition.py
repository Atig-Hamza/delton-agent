"""
╔══════════════════════════════════════════════════╗
║  Skill 08: Composition & Framing Helpers         ║
╚══════════════════════════════════════════════════╝
"""

from typing import Tuple, List


class CompositionHelper:
    """Utility functions for layout, positioning, and framing."""

    @staticmethod
    def percent_to_pixels(x_pct: float, y_pct: float,
                          width: int, height: int) -> Tuple[int, int]:
        """Convert percentage position (0–100) to absolute pixel coordinates."""
        x = int(x_pct / 100.0 * width)
        y = int(y_pct / 100.0 * height)
        return x, y

    @staticmethod
    def rule_of_thirds(width: int, height: int) -> dict:
        """Return the 9 rule-of-thirds grid intersection points."""
        return {
            "top_left":     (width // 3,       height // 3),
            "top_center":   (width // 2,       height // 3),
            "top_right":    (2 * width // 3,   height // 3),
            "mid_left":     (width // 3,       height // 2),
            "center":       (width // 2,       height // 2),
            "mid_right":    (2 * width // 3,   height // 2),
            "bot_left":     (width // 3,       2 * height // 3),
            "bot_center":   (width // 2,       2 * height // 3),
            "bot_right":    (2 * width // 3,   2 * height // 3),
        }

    @staticmethod
    def clamp(value: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, value))

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Smooth ease-out cubic (0→1)."""
        t = CompositionHelper.clamp(t, 0.0, 1.0)
        return 1 - (1 - t) ** 3

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Smooth ease-in-out (0→1)."""
        t = CompositionHelper.clamp(t, 0.0, 1.0)
        return t * t * (3 - 2 * t)

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    @staticmethod
    def get_text_bbox(draw, text: str, font) -> Tuple[int, int]:
        """Return (width, height) of text bounding box — works with PIL ≥9 and older."""
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            # PIL < 9 fallback
            return draw.textsize(text, font=font)
