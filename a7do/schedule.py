# a7do/schedule.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from a7do.events import ExperienceEvent


class Schedule:
    """
    Executes the day's events.
    Enforces: day must end at home in bed, then sleep.
    """

    def __init__(self):
        self.day: int = 0
        self.state: str = "sleeping"  # sleeping | awake
        self.events: List[ExperienceEvent] = []
        self.index: int = 0

        self.current_place: str = "hospital"
        self.current_room: str = "ward"

        self.movements: List[Dict[str, Any]] = []  # A7DO movement log (observer-visible)

    def load(self, day: int, events: List[ExperienceEvent], start_place: str, start_room: str):
        self.day = day
        self.events = list(events)
        self.index = 0
        self.current_place = start_place
        self.current_room = start_room
        self.state = "sleeping"  # must wake explicitly

    def authorise_wake(self):
        self.state = "awake"

    def next_event(self) -> Optional[ExperienceEvent]:
        if self.state != "awake":
            return None
        if self.index >= len(self.events):
            return None
        ev = self.events[self.index]
        self.index += 1

        # Track movement if present
        mv = ev.movement or {}
        if mv.get("from") and mv.get("to"):
            self.movements.append({
                "day": self.day,
                "event": self.index,
                "actor": "A7DO",
                "from": mv["from"],
                "to": mv["to"]
            })
            self.current_place = mv["to"]
            self.current_room = ev.room or self.current_room
        else:
            self.current_place = ev.place_id or self.current_place
            self.current_room = ev.room or self.current_room

        return ev

    def end_day_enforced(self):
        """
        Force final location = home bedroom bed.
        This is the invariant you requested.
        """
        self.current_place = "bedroom_a7do"
        self.current_room = "bed"
        self.state = "sleeping"

    def status(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "state": self.state,
            "event_index": self.index,
            "events_total": len(self.events),
            "current_place": self.current_place,
            "current_room": self.current_room,
            "movements": len(self.movements),
        }