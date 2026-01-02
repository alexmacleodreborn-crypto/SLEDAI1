#a7do/schedule.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from a7do.body import BiologicalState
from a7do.events import ExperienceEvent

@dataclass
class SpatialState:
    place_id: str = "hospital_cwh"
    room: str = "delivery_room"
    pos_xyz: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    locomotion: str = "newborn"

class Schedule:
    def __init__(self):
        self.day: int = 0
        self.state: str = "waiting"  # waiting | awake | asleep | complete
        self.queue: List[ExperienceEvent] = []
        self.spatial = SpatialState()
        self.body = BiologicalState()

    def load(self, day: int, events: List[ExperienceEvent], start_place="hospital_cwh", start_room="delivery_room"):
        self.day = day
        self.queue = list(events)
        self.state = "waiting"
        self.spatial.place_id = start_place
        self.spatial.room = start_room
        if start_place and start_place != self.spatial.place_id:
            self.spatial.place_id = start_place

    def authorise_wake(self):
        if self.day == 0 and self.spatial.place_id != "hospital_cwh":
            self.spatial.place_id = "hospital_cwh"
            self.spatial.room = "delivery_room"
        self.state = "awake"

    def next_event(self) -> Optional[ExperienceEvent]:
        if self.queue:
            return self.queue.pop(0)
        return None

    def sleep(self):
        self.state = "asleep"

    def complete(self):
        self.state = "complete"

    def status(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "state": self.state,
            "place_id": self.spatial.place_id,
            "room": self.spatial.room,
            "pos_xyz": self.spatial.pos_xyz,
            "locomotion": self.spatial.locomotion,
            "events_remaining": len(self.queue),
            "body": self.body.snapshot(),
        }