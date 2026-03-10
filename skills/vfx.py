"""
╔══════════════════════════════════════════════════╗
║  Skill 09: Visual Effects (VFX)                  ║
╚══════════════════════════════════════════════════╝
"""

import numpy as np
from PIL import Image, ImageFilter


class VFXEngine:
    """Applies real-time visual effects to PIL Images."""

    def apply(self, img: Image.Image, effect: str, t: float, duration: float) -> Image.Image:
        """Dispatch to the right effect handler. Unknown effects are silently skipped."""
        handler = getattr(self, f"_fx_{effect}", None)
        if handler:
            try:
                img = handler(img, t, duration)
            except Exception:
                pass
        return img

    # ─── Vignette ────────────────────────────────────
    def _fx_vignette(self, img, t, duration):
        w, h = img.size
        arr = np.array(img.convert("RGB")).astype(np.float32)
        cx, cy = w / 2, h / 2
        Y, X = np.ogrid[:h, :w]
        dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
        vignette = np.clip(1.0 - 0.6 * dist, 0, 1)[..., np.newaxis]
        arr = arr * vignette
        result = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        if img.mode == "RGBA":
            result.putalpha(img.split()[3])
        return result

    # ─── Film Grain ───────────────────────────────────
    def _fx_film_grain(self, img, t, duration):
        arr = np.array(img.convert("RGB")).astype(np.float32)
        noise = np.random.normal(0, 8, arr.shape).astype(np.float32)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        result = Image.fromarray(arr)
        if img.mode == "RGBA":
            result.putalpha(img.split()[3])
        return result

    # ─── Chromatic Aberration ─────────────────────────
    def _fx_chromatic_aberration(self, img, t, duration):
        rgb = img.convert("RGB")
        r, g, b = rgb.split()
        offset = 3
        r = r.transform(r.size, Image.AFFINE, (1, 0, -offset, 0, 1, 0))
        b = b.transform(b.size, Image.AFFINE, (1, 0,  offset, 0, 1, 0))
        result = Image.merge("RGB", (r, g, b))
        if img.mode == "RGBA":
            result.putalpha(img.split()[3])
        return result

    # ─── Glow / Bloom ─────────────────────────────────
    def _fx_glow(self, img, t, duration):
        base = img.convert("RGB")
        blurred = base.filter(ImageFilter.GaussianBlur(radius=12))
        arr_b = np.array(base).astype(np.float32)
        arr_g = np.array(blurred).astype(np.float32)
        arr = np.clip(arr_b + arr_g * 0.25, 0, 255).astype(np.uint8)
        result = Image.fromarray(arr)
        if img.mode == "RGBA":
            result.putalpha(img.split()[3])
        return result

    # ─── Lens Flare (simple) ─────────────────────────
    def _fx_lens_flare(self, img, t, duration):
        from PIL import ImageDraw
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        w, h = img.size
        cx, cy = int(w * 0.3), int(h * 0.25)
        for radius, alpha in [(80, 30), (50, 50), (20, 80)]:
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=(255, 240, 200, alpha),
            )
        base = img.convert("RGBA")
        result = Image.alpha_composite(base, overlay)
        if img.mode != "RGBA":
            result = result.convert(img.mode)
        return result

    # ─── Light Rays ───────────────────────────────────
    def _fx_light_rays(self, img, t, duration):
        from PIL import ImageDraw
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        w, h = img.size
        for i in range(8):
            angle = i * 45
            import math
            dx = int(w * math.cos(math.radians(angle)) * 1.5)
            dy = int(h * math.sin(math.radians(angle)) * 1.5)
            draw.line([(w // 2, 0), (w // 2 + dx, dy)], fill=(255, 240, 180, 20), width=30)
        base = img.convert("RGBA")
        result = Image.alpha_composite(base, overlay)
        if img.mode != "RGBA":
            result = result.convert(img.mode)
        return result

    # ─── Blur Background ──────────────────────────────
    def _fx_blur_background(self, img, t, duration):
        blurred = img.filter(ImageFilter.GaussianBlur(radius=8))
        # In a real implementation, only the background would be blurred.
        # This is a full-frame blur as a placeholder.
        return blurred

    # ─── Screen Shake ─────────────────────────────────
    def _fx_screen_shake(self, img, t, duration):
        import random
        dx = random.randint(-6, 6)
        dy = random.randint(-6, 6)
        return img.transform(img.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))

    # ─── Particles (simple overlay) ──────────────────
    def _particles_overlay(self, img, t, color, count=40):
        from PIL import ImageDraw
        import random
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        w, h = img.size
        rng = random.Random(int(t * 30))
        for _ in range(count):
            x = rng.randint(0, w)
            y = int((rng.randint(0, h) - t * 60) % h)
            r = rng.randint(2, 6)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
        base = img.convert("RGBA")
        result = Image.alpha_composite(base, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result

    def _fx_particles_dust(self, img, t, duration):
        return self._particles_overlay(img, t, (200, 190, 170, 80), 30)

    def _fx_particles_sparks(self, img, t, duration):
        return self._particles_overlay(img, t, (255, 180, 50, 180), 25)

    def _fx_particles_bokeh(self, img, t, duration):
        return self._particles_overlay(img, t, (255, 255, 200, 60), 20)

    def _fx_particles_snow(self, img, t, duration):
        return self._particles_overlay(img, t, (255, 255, 255, 160), 40)

    def _fx_particles_rain(self, img, t, duration):
        from PIL import ImageDraw
        import random
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        w, h = img.size
        rng = random.Random(int(t * 30))
        for _ in range(80):
            x = rng.randint(0, w)
            y = int((rng.randint(0, h) + t * 150) % h)
            draw.line([(x, y), (x - 1, y + 10)], fill=(180, 200, 255, 100), width=1)
        base = img.convert("RGBA")
        result = Image.alpha_composite(base, overlay)
        return result.convert(img.mode) if img.mode != "RGBA" else result
