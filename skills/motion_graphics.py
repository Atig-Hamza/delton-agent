"""
╔══════════════════════════════════════════════════╗
║  Skill 05: Motion Graphics & Text Rendering      ║
╚══════════════════════════════════════════════════╝
"""

import math
import numpy as np
from PIL import Image, ImageDraw

from skills.composition import CompositionHelper


class MotionGraphicsEngine:
    """
    Renders animated text, icons, shapes, counters and progress bars
    onto a PIL Image given the current time `t` within a scene.
    """

    def __init__(self, asset_manager=None):
        self._asset_manager = asset_manager  # injected by renderer
        self._comp = CompositionHelper()

    def set_asset_manager(self, asset_manager):
        self._asset_manager = asset_manager

    # ─── Public entry point ───────────────────────────
    def render_element(self, img: Image.Image, element: dict,
                       t: float, duration: float) -> Image.Image:
        """Render one element onto img at time t and return the updated image."""
        elem_type = element.get("type", "text")

        # Compute animation alpha and position offset
        alpha, offset = self._compute_animation(element, t, duration)
        if alpha <= 0:
            return img

        if elem_type == "text":
            img = self._draw_text(img, element, alpha, offset)
        elif elem_type == "icon":
            img = self._draw_icon(img, element, alpha, offset)
        elif elem_type == "shape":
            img = self._draw_shape(img, element, alpha, offset)
        elif elem_type == "counter":
            img = self._draw_counter(img, element, t, duration, alpha, offset)
        elif elem_type == "progress_bar":
            img = self._draw_progress_bar(img, element, t, duration, alpha, offset)

        return img

    # ─── Animation timing ─────────────────────────────
    def _compute_animation(self, element: dict, t: float, duration: float):
        """
        Return (alpha 0–1, offset_pixels (dx, dy)) for the current time.
        Handles fade_in, slide_up/down/left/right, scale_up, typewriter, etc.
        """
        anim_in      = element.get("animation_in", "fade_in")
        delay_in     = float(element.get("animation_in_delay", 0.0))
        dur_in       = float(element.get("animation_in_duration", 0.4))
        delay_out    = float(element.get("animation_out_delay", duration * 0.8))
        dur_out      = float(element.get("animation_out_duration", 0.3))

        # Animation-in progress
        if t < delay_in:
            return 0.0, (0, 0)

        t_in = t - delay_in
        if t_in < dur_in and dur_in > 0:
            p = self._comp.ease_out_cubic(t_in / dur_in)
        else:
            p = 1.0

        # Animation-out progress
        if t >= delay_out:
            t_out = t - delay_out
            p_out = self._comp.ease_in_out(t_out / max(dur_out, 0.01))
            p_out = min(p_out, 1.0)
        else:
            p_out = 0.0

        alpha = p * (1.0 - p_out)
        offset = self._anim_offset(anim_in, p, element)
        return alpha, offset

    def _anim_offset(self, anim_in: str, progress: float, element: dict):
        """Return (dx, dy) pixel offset based on animation type."""
        dist = 60  # slide distance in pixels
        inv = 1.0 - progress
        if anim_in == "slide_up":
            return (0, int(dist * inv))
        if anim_in == "slide_down":
            return (0, -int(dist * inv))
        if anim_in == "slide_left":
            return (int(dist * inv), 0)
        if anim_in == "slide_right":
            return (-int(dist * inv), 0)
        return (0, 0)

    # ─── Text ─────────────────────────────────────────
    def _draw_text(self, img: Image.Image, element: dict,
                   alpha: float, offset: tuple) -> Image.Image:
        content = element.get("content", "")
        if not content:
            return img

        w, h = img.size
        pos_x, pos_y = self._comp.percent_to_pixels(
            element.get("position", [50, 50])[0],
            element.get("position", [50, 50])[1],
            w, h,
        )
        pos_x += offset[0]
        pos_y += offset[1]

        color = tuple(element.get("color", [255, 255, 255]))
        size_scale = float(element.get("size", 1.0))
        base_size = self._base_text_size(w, h, element)
        font_size = max(10, int(base_size * size_scale))

        font_key = element.get("font", "heading") or "heading"
        font = self._get_font(font_key, font_size)

        # Special animations
        anim = element.get("animation_in", "fade_in")

        # Typewriter — reveal characters
        if anim == "typewriter":
            visible_chars = max(1, int(len(content) * alpha))
            content = content[:visible_chars]
            alpha = 1.0  # text is always fully opaque once shown

        # Scale-up animation — we approximate by changing font size
        if anim == "scale_up":
            anim_in_dur = float(element.get("animation_in_duration", 0.4))
            font_size = max(10, int(font_size * (0.5 + 0.5 * alpha)))
            font = self._get_font(font_key, font_size)

        # Build RGBA overlay
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        tw, th = self._comp.get_text_bbox(draw, content, font)
        x = pos_x - tw // 2
        y = pos_y - th // 2

        text_alpha = int(255 * min(alpha, 1.0))
        rgba_color = (*color[:3], text_alpha)

        draw.text((x, y), content, font=font, fill=rgba_color)

        base_rgba = img.convert("RGBA")
        result = Image.alpha_composite(base_rgba, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result

    def _base_text_size(self, width: int, height: int, element: dict) -> int:
        """Determine a sensible base font size from element type/content."""
        content = element.get("content", "")
        # Shorter text → larger size
        if len(content) <= 10:
            return max(36, width // 20)
        if len(content) <= 30:
            return max(28, width // 30)
        return max(20, width // 40)

    # ─── Icon ─────────────────────────────────────────
    def _draw_icon(self, img: Image.Image, element: dict,
                   alpha: float, offset: tuple) -> Image.Image:
        """Render a Lucide SVG icon, or fall back to a colored circle placeholder."""
        icon_name = element.get("icon_name", element.get("content", "zap"))
        w, h = img.size
        pos_x, pos_y = self._comp.percent_to_pixels(
            element.get("position", [50, 50])[0],
            element.get("position", [50, 50])[1],
            w, h,
        )
        pos_x += offset[0]
        pos_y += offset[1]

        size_scale = float(element.get("size", 1.0))
        icon_size = max(20, int(min(w, h) * 0.08 * size_scale))
        color = tuple(element.get("color", [255, 255, 255]))

        # Try SVG rendering
        svg_data = None
        if self._asset_manager:
            svg_data = self._asset_manager.get_icon_svg(icon_name)

        if svg_data:
            try:
                import cairosvg
                from io import BytesIO
                png_data = cairosvg.svg2png(
                    bytestring=svg_data,
                    output_width=icon_size,
                    output_height=icon_size,
                )
                icon_img = Image.open(BytesIO(png_data)).convert("RGBA")
                # Tint icon
                icon_arr = np.array(icon_img).astype(np.float32)
                for c_idx, c_val in enumerate(color[:3]):
                    icon_arr[..., c_idx] = icon_arr[..., c_idx] * (c_val / 255.0)
                icon_arr[..., 3] = icon_arr[..., 3] * alpha
                icon_img = Image.fromarray(np.clip(icon_arr, 0, 255).astype(np.uint8))
                x = pos_x - icon_size // 2
                y = pos_y - icon_size // 2
                base = img.convert("RGBA")
                base.paste(icon_img, (x, y), icon_img)
                return base.convert(img.mode) if img.mode != "RGBA" else base
            except Exception:
                pass

        # Fallback: draw a colored circle
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        x0 = pos_x - icon_size // 2
        y0 = pos_y - icon_size // 2
        x1 = pos_x + icon_size // 2
        y1 = pos_y + icon_size // 2
        fill = (*color[:3], int(255 * alpha))
        draw.ellipse([x0, y0, x1, y1], fill=fill)

        base_rgba = img.convert("RGBA")
        result = Image.alpha_composite(base_rgba, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result

    # ─── Shape ────────────────────────────────────────
    def _draw_shape(self, img: Image.Image, element: dict,
                    alpha: float, offset: tuple) -> Image.Image:
        w, h = img.size
        pos_x, pos_y = self._comp.percent_to_pixels(
            element.get("position", [50, 50])[0],
            element.get("position", [50, 50])[1],
            w, h,
        )
        pos_x += offset[0]
        pos_y += offset[1]

        size_scale = float(element.get("size", 1.0))
        shape_w = int(w * 0.15 * size_scale)
        shape_h = int(h * 0.05 * size_scale)
        color = tuple(element.get("color", [255, 255, 255]))
        shape_type = element.get("content", "rectangle")

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        fill = (*color[:3], int(255 * alpha))
        x0 = pos_x - shape_w // 2
        y0 = pos_y - shape_h // 2
        x1 = pos_x + shape_w // 2
        y1 = pos_y + shape_h // 2

        if shape_type == "circle":
            r = min(shape_w, shape_h) // 2
            draw.ellipse([pos_x - r, pos_y - r, pos_x + r, pos_y + r], fill=fill)
        elif shape_type == "line":
            draw.line([x0, pos_y, x1, pos_y], fill=fill, width=max(2, shape_h // 4))
        else:  # rectangle / default
            draw.rectangle([x0, y0, x1, y1], fill=fill)

        base_rgba = img.convert("RGBA")
        result = Image.alpha_composite(base_rgba, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result

    # ─── Counter ──────────────────────────────────────
    def _draw_counter(self, img: Image.Image, element: dict,
                      t: float, duration: float,
                      alpha: float, offset: tuple) -> Image.Image:
        start_val = int(element.get("counter_start", 0) or 0)
        end_val   = int(element.get("counter_end", 100) or 100)
        progress  = self._comp.ease_out_cubic(min(t / max(duration * 0.8, 0.01), 1.0))
        current   = int(start_val + (end_val - start_val) * progress)

        elem = dict(element)
        elem["content"] = str(current)
        elem["type"] = "text"
        return self._draw_text(img, elem, alpha, offset)

    # ─── Progress Bar ─────────────────────────────────
    def _draw_progress_bar(self, img: Image.Image, element: dict,
                           t: float, duration: float,
                           alpha: float, offset: tuple) -> Image.Image:
        w, h = img.size
        pos_x, pos_y = self._comp.percent_to_pixels(
            element.get("position", [50, 80])[0],
            element.get("position", [50, 80])[1],
            w, h,
        )
        pos_x += offset[0]
        pos_y += offset[1]

        bar_w = int(w * 0.4 * float(element.get("size", 1.0)))
        bar_h = max(6, h // 60)
        progress = self._comp.ease_out_cubic(min(t / max(duration * 0.7, 0.01), 1.0))
        color = tuple(element.get("color", [100, 200, 255]))

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        x0 = pos_x - bar_w // 2
        y0 = pos_y - bar_h // 2
        x1 = pos_x + bar_w // 2
        y1 = pos_y + bar_h // 2

        bg_alpha = int(80 * alpha)
        draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, bg_alpha))

        fill_x1 = x0 + int((x1 - x0) * progress)
        if fill_x1 > x0:
            fill_alpha = int(220 * alpha)
            draw.rectangle([x0, y0, fill_x1, y1], fill=(*color[:3], fill_alpha))

        base_rgba = img.convert("RGBA")
        result = Image.alpha_composite(base_rgba, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result

    # ─── Font helper ──────────────────────────────────
    def _get_font(self, font_key: str, size: int):
        if self._asset_manager:
            return self._asset_manager.get_font(font_key, size)
        # Minimal fallback
        try:
            from PIL import ImageFont
            fallbacks = [
                r"C:\Windows\Fonts\arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
            for fp in fallbacks:
                import os
                if os.path.exists(fp):
                    return ImageFont.truetype(fp, size)
            return ImageFont.load_default()
        except Exception:
            from PIL import ImageFont
            return ImageFont.load_default()
