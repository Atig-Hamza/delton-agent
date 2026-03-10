"""
╔══════════════════════════════════════════════════╗
║  Skill 06: Audio & Beat Sync                     ║
╚══════════════════════════════════════════════════╝
"""

import numpy as np
from typing import Optional


class AudioSync:
    """Audio processing and beat-sync utilities."""

    def generate_silence(self, duration: float, fps: int = 44100) -> np.ndarray:
        """Return a silent numpy audio array (stereo)."""
        samples = int(duration * fps)
        return np.zeros((samples, 2), dtype=np.float32)

    def beats_from_bpm(self, bpm: int, duration: float) -> list:
        """Return a list of beat timestamps for a given BPM and duration."""
        interval = 60.0 / max(bpm, 1)
        beats = []
        t = 0.0
        while t <= duration:
            beats.append(t)
            t += interval
        return beats

    def detect_beats(self, audio_path: str) -> list:
        """Try to detect beat timestamps from an audio file (requires librosa)."""
        try:
            import librosa
            y, sr = librosa.load(audio_path, sr=None)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()
            return beat_times
        except Exception:
            return []

    def sync_cuts_to_beats(self, scenes: list, bpm: int) -> list:
        """
        Adjust scene durations to snap to beat boundaries.
        Returns a new list of scenes with adjusted start/end times.
        """
        beat_interval = 60.0 / max(bpm, 1)
        adjusted = []
        cursor = 0.0
        for scene in scenes:
            raw_dur = scene.get("duration", 3.0)
            # Snap to nearest beat multiple
            beats_needed = max(1, round(raw_dur / beat_interval))
            snapped_dur = beats_needed * beat_interval
            s = dict(scene)
            s["start_time"] = cursor
            s["duration"] = snapped_dur
            s["end_time"] = cursor + snapped_dur
            adjusted.append(s)
            cursor += snapped_dur
        return adjusted
