"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Multi-format Export Module             ║
╚══════════════════════════════════════════════════╝
"""

import os
import time


class Exporter:
    """Handles multi-format video export from a MoviePy clip."""

    SUPPORTED_FORMATS = {
        "mp4":  {"codec": "libx264",  "audio_codec": "aac"},
        "webm": {"codec": "libvpx",   "audio_codec": "libvorbis"},
        "mov":  {"codec": "libx264",  "audio_codec": "aac"},
        "gif":  {"codec": None,       "audio_codec": None},
    }

    DEFAULT_BITRATE = "8000k"
    DEFAULT_FPS = 30

    def export(self, clip, output_path: str, settings: dict = None) -> str:
        """
        Write a MoviePy VideoClip to disk.

        Args:
            clip:         MoviePy VideoClip instance.
            output_path:  Full destination path including extension.
            settings:     Optional dict with keys: format, codec, bitrate, fps, audio.

        Returns:
            str: The final output path.
        """
        settings = settings or {}
        fmt = settings.get("format", "mp4").lower()
        fps = settings.get("fps", self.DEFAULT_FPS)
        bitrate = settings.get("bitrate", self.DEFAULT_BITRATE)
        include_audio = settings.get("audio", True)

        fmt_info = self.SUPPORTED_FORMATS.get(fmt, self.SUPPORTED_FORMATS["mp4"])
        codec = settings.get("codec", fmt_info["codec"])
        audio_codec = fmt_info["audio_codec"]

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if fmt == "gif":
            clip.write_gif(output_path, fps=min(fps, 15), verbose=False, logger=None)
        else:
            clip.write_videofile(
                output_path,
                fps=fps,
                codec=codec,
                bitrate=bitrate,
                audio=include_audio,
                audio_codec=audio_codec if include_audio else None,
                verbose=False,
                logger=None,
            )

        return output_path

    def get_output_path(self, project_name: str, fmt: str = "mp4",
                        output_dir: str = "output") -> str:
        """Generate a timestamped output path."""
        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in project_name)
        filename = f"{safe_name}_{int(time.time())}.{fmt}"
        return os.path.join(output_dir, filename)
