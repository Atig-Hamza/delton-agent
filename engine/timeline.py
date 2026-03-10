"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Timeline Management                    ║
╚══════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class SceneEntry:
    scene_id: int
    name: str
    start_time: float
    end_time: float
    duration: float
    scene_data: Dict[str, Any]


class Timeline:
    """Manages the ordered sequence of scenes and their timing."""

    def __init__(self):
        self.scenes: List[SceneEntry] = []
        self.total_duration: float = 0.0
        self.fps: int = 30
        self.resolution: tuple = (1920, 1080)
        self.plan: Optional[Dict] = None

    def build_from_plan(self, plan: Dict[str, Any]):
        """Build the timeline from an AI-generated plan."""
        self.plan = plan
        self.scenes = []
        self.fps = plan.get("fps", 30)
        resolution_list = plan.get("resolution", [1920, 1080])
        self.resolution = tuple(resolution_list)
        self.total_duration = plan.get("total_duration", 0.0)

        for scene_data in plan.get("scenes", []):
            duration = scene_data.get("duration", 3.0)
            start = scene_data.get("start_time", 0.0)
            end = scene_data.get("end_time", start + duration)
            entry = SceneEntry(
                scene_id=scene_data.get("scene_id", 0),
                name=scene_data.get("name", "Scene"),
                start_time=start,
                end_time=end,
                duration=duration,
                scene_data=scene_data,
            )
            self.scenes.append(entry)

    def get_scene_at(self, time: float) -> Optional[SceneEntry]:
        for scene in self.scenes:
            if scene.start_time <= time < scene.end_time:
                return scene
        return None

    def get_total_frames(self) -> int:
        return int(self.total_duration * self.fps)

    def __len__(self):
        return len(self.scenes)

    def __iter__(self):
        return iter(self.scenes)
