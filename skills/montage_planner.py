"""
╔══════════════════════════════════════════════════╗
║  Skill 02: Montage Architecture Planner          ║
╚══════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List


class MontagePlanner:
    """Validates and pre-processes an AI-generated montage plan."""

    REQUIRED_FIELDS = ["project_name", "format", "resolution", "fps",
                       "total_duration", "scenes"]

    def validate(self, plan: dict) -> List[str]:
        """Return a list of validation errors (empty = OK)."""
        errors = []
        for field in self.REQUIRED_FIELDS:
            if field not in plan:
                errors.append(f"Missing required field: {field}")

        scenes = plan.get("scenes", [])
        if not scenes:
            errors.append("Plan has no scenes.")

        for i, scene in enumerate(scenes):
            if "duration" not in scene:
                errors.append(f"Scene {i} missing 'duration'.")
            if "elements" not in scene:
                errors.append(f"Scene {i} missing 'elements'.")

        return errors

    def normalize(self, plan: dict) -> dict:
        """Fill in defaults for missing optional fields and return a clean plan."""
        plan.setdefault("fps", 30)
        plan.setdefault("color_grade", None)
        plan.setdefault("ad_style", None)
        plan.setdefault("music", {"style": "ambient", "bpm": 120, "mood": "neutral"})
        plan.setdefault("global_effects", {})
        plan.setdefault("export", {
            "format": "mp4",
            "codec": "libx264",
            "bitrate": "8000k",
            "audio": True,
        })

        # Normalize scenes
        cursor = 0.0
        for scene in plan.get("scenes", []):
            scene.setdefault("start_time", cursor)
            duration = scene.get("duration", 3.0)
            scene.setdefault("end_time", cursor + duration)
            scene.setdefault("elements", [])
            scene.setdefault("vfx", [])
            scene.setdefault("sound_effects", [])
            scene.setdefault("speed_effect", "normal")
            scene.setdefault("speed_value", 1.0)
            scene.setdefault("transition_in", None)
            scene.setdefault("transition_in_duration", 0.5)
            scene.setdefault("transition_out", None)
            scene.setdefault("transition_out_duration", 0.5)
            scene.setdefault("background", {"type": "solid", "color": [10, 10, 20]})
            cursor += duration

        return plan

    def prepare(self, plan: dict) -> dict:
        """Validate then normalize a plan. Raises ValueError on critical errors."""
        errors = self.validate(plan)
        critical = [e for e in errors if "Missing required field" in e or "no scenes" in e]
        if critical:
            raise ValueError(f"Plan validation failed: {'; '.join(critical)}")
        return self.normalize(plan)
