# world_frame/world_state.py

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class WorldEvent:
    time: float
    place: str
    description: str
    tags: List[str] = field(default_factory=list)


@dataclass
class WorldState:
    """
    Objective world state.
    This is ground truth, not A7DO's understanding.
    """

    # --- Core world timeline ---
    day: int = 0
    time: float = 0.0  # 0.0–24.0
    birthed: bool = False

    # --- Location ---
    current_place: str = "Hospital"

    # --- History ---
    events: List[WorldEvent] = field(default_factory=list)

    # -------------------------------------------------
    # World transitions
    # -------------------------------------------------

    def register_birth(self):
        """
        Birth is a WORLD event, not a mental one.
        """
        if not self.birthed:
            self.birthed = True
            self.current_place = "Hospital"
            self.events.append(
                WorldEvent(
                    time=self.time,
                    place="Hospital",
                    description="A7DO birth event",
                    tags=["birth", "hospital"],
                )
            )

    def move_to(self, place: str, description: str = ""):
        """
        Physical movement in the world.
        """
        self.current_place = place
        self.events.append(
            WorldEvent(
                time=self.time,
                place=place,
                description=description or f"Moved to {place}",
                tags=["movement"],
            )
        )

    def tick(self, delta: float = 0.5):
        """
        Advance world time.
        """
        self.time += delta
        if self.time >= 24.0:
            self.time = 0.0
            self.day += 1

    # -------------------------------------------------
    # Observer-safe snapshot
    # -------------------------------------------------

    def snapshot(self) -> Dict:
        return {
            "day": self.day,
            "time": round(self.time, 2),
            "place": self.current_place,
            "birthed": self.birthed,
            "event_count": len(self.events),
        }