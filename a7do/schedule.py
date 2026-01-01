from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from a7do.body import BiologicalState
from a7do.events import ExperienceEvent

@dataclass
class SpatialState:
    building: str = "House_A7DO"
    room: str = "hall"
    pos_xy: Tuple[float, float] = (0.5, 0.5)
    locomotion: str = "crawl"

class Schedule:
    """
    Always-present time container.
    """
    def __init__(self):
        self.day: int = 0
        self.state: str = "waiting"  # waiting | awake | asleep | complete
        self.events: List[ExperienceEvent] = []
        self.spatial = SpatialState()
        self.body = BiologicalState()

        self.world_seed: int = 42
        self.world_ready: bool = False

    def load_day(self, day: int, events: List[ExperienceEvent], start_room="hall"):
        self.day = day
        self.events = list(events)
        self.state = "waiting"
        self.spatial.building = "House_A7DO"
        self.spatial.room = start_room
        self.spatial.pos_xy = (0.5, 0.5)

    def wake(self):
        self.state = "awake"

    def next_event(self) -> Optional[ExperienceEvent]:
        if self.events:
            return self.events.pop(0)
        return None

    def sleep(self):
        self.state = "asleep"

    def complete(self):
        self.state = "complete"

    def status(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "state": self.state,
            "building": self.spatial.building,
            "room": self.spatial.room,
            "pos_xy": self.spatial.pos_xy,
            "locomotion": self.spatial.locomotion,
            "events_remaining": len(self.events),
            "body": self.body.snapshot(),
        }