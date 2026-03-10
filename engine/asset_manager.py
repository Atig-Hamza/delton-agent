"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Asset Manager — Icons, Fonts, Assets   ║
╚══════════════════════════════════════════════════╝
"""

import os
from typing import Optional, Dict

try:
    import requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

from PIL import ImageFont
from config import FONTS_DIR, ICONS_DIR, ICON_LIBRARIES, FONTS


class AssetManager:
    """Manages fonts, icons, and other project assets."""

    def __init__(self):
        self._font_cache: Dict[str, ImageFont.ImageFont] = {}
        self._icon_cache: Dict[str, bytes] = {}
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(FONTS_DIR, exist_ok=True)
        os.makedirs(ICONS_DIR, exist_ok=True)

    # ─── Fonts ──────────────────────────────────────────
    def get_font(self, font_key: str = "heading", size: int = 48) -> ImageFont.ImageFont:
        """Return a PIL ImageFont; falls back to built-in default."""
        cache_key = f"{font_key}_{size}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        font_name = FONTS.get(font_key, "Arial-Bold")
        font_path = os.path.join(FONTS_DIR, f"{font_name}.ttf")

        font = None
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, size)
            except Exception:
                pass

        # System font fallbacks (Windows → Linux → macOS)
        if font is None:
            fallbacks = [
                r"C:\Windows\Fonts\arialbd.ttf",
                r"C:\Windows\Fonts\arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
            ]
            for fp in fallbacks:
                if os.path.exists(fp):
                    try:
                        font = ImageFont.truetype(fp, size)
                        break
                    except Exception:
                        pass

        if font is None:
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font

    def get_font_by_size(self, size: int = 48) -> ImageFont.ImageFont:
        return self.get_font("heading", size)

    # ─── Icons ──────────────────────────────────────────
    def get_icon_svg(self, icon_name: str) -> Optional[bytes]:
        """Return SVG bytes for a Lucide icon, downloading if necessary."""
        if icon_name in self._icon_cache:
            return self._icon_cache[icon_name]

        icon_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
        if os.path.exists(icon_path):
            with open(icon_path, "rb") as f:
                data = f.read()
            self._icon_cache[icon_name] = data
            return data

        if not _REQUESTS_AVAILABLE:
            return None

        library = ICON_LIBRARIES.get("lucide", {})
        base_url = library.get("base_url", "")
        icons = library.get("icons", {})
        svg_file = icons.get(icon_name, f"{icon_name}.svg")
        url = base_url + svg_file

        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.content
                with open(icon_path, "wb") as f:
                    f.write(data)
                self._icon_cache[icon_name] = data
                return data
        except Exception:
            pass

        return None
