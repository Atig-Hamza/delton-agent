"""
╔══════════════════════════════════════════════════╗
║  Skill 01: Scene Analysis                        ║
╚══════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List


class SceneAnalyzer:
    """Analyzes a scene dict and surfaces metadata for the renderer."""

    # Scene types ranked by visual intensity
    INTENSITY_MAP = {
        "hook": 1.0,
        "climax": 0.95,
        "cta": 0.9,
        "build": 0.75,
        "content": 0.5,
        "intro": 0.4,
        "outro": 0.3,
    }

    def analyze(self, scene: dict) -> Dict[str, Any]:
        """Return a metadata dict about a scene."""
        scene_type = scene.get("type", "content")
        elements = scene.get("elements", [])
        vfx = scene.get("vfx", [])

        return {
            "scene_id": scene.get("scene_id", 0),
            "type": scene_type,
            "intensity": self.INTENSITY_MAP.get(scene_type, 0.5),
            "element_count": len(elements),
            "has_text": any(e.get("type") == "text" for e in elements),
            "has_icon": any(e.get("type") == "icon" for e in elements),
            "has_shape": any(e.get("type") == "shape" for e in elements),
            "has_counter": any(e.get("type") == "counter" for e in elements),
            "vfx_count": len(vfx),
            "is_premium": len(vfx) >= 2 or scene_type in ("hook", "climax"),
            "duration": scene.get("duration", 3.0),
        }

    def analyze_plan(self, plan: dict) -> List[Dict[str, Any]]:
        """Analyze all scenes in a plan."""
        return [self.analyze(s) for s in plan.get("scenes", [])]
