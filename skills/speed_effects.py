"""
╔══════════════════════════════════════════════════╗
║  Skill 07: Speed Ramping & Effects               ║
╚══════════════════════════════════════════════════╝
"""


class SpeedEffects:
    """Applies speed manipulations to MoviePy clips."""

    def apply(self, clip, effect: str, value: float = 1.0):
        """Apply speed effect to a clip. Returns modified clip."""
        try:
            from moviepy.video.fx.all import speedx
        except ImportError:
            return clip

        if effect == "slow_motion":
            factor = value if 0 < value < 1 else 0.5
            return clip.fx(speedx, factor)

        if effect == "fast":
            factor = value if value > 1 else 2.0
            return clip.fx(speedx, factor)

        if effect == "speed_ramp":
            # Simple two-phase ramp: start slow, end fast
            half = clip.duration / 2
            first = clip.subclip(0, half).fx(speedx, 0.5)
            second = clip.subclip(half).fx(speedx, 2.0)
            from moviepy.editor import concatenate_videoclips
            return concatenate_videoclips([first, second])

        if effect == "reverse":
            return clip.fx(lambda c: c.fl_time(lambda t: c.duration - t, keep_duration=True))

        if effect == "freeze_frame":
            freeze_t = clip.duration / 2
            freeze = clip.to_ImageClip(t=freeze_t).set_duration(1.0)
            from moviepy.editor import concatenate_videoclips
            return concatenate_videoclips([clip, freeze])

        # Default: normal
        return clip

    def slow_motion(self, clip, factor: float = 0.5):
        return self.apply(clip, "slow_motion", factor)

    def fast_forward(self, clip, factor: float = 2.0):
        return self.apply(clip, "fast", factor)
