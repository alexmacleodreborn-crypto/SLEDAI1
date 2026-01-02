# a7do_core/perceived_world_state.py

from dataclasses import dataclass, field
from typing import Dict, Optional, List


@dataclass
class PlaceMemory:
    visits: int = 0
    exposure: float = 0.0          # accumulated exposure time
    familiarity: float = 0.0       # 0..1
    comfort_bias: float = 0.0      # -1..+1 (only from affect tags)
    last_day_seen: int = 0


@dataclass
class PerceivedWorldState:
    """
    Subjective awareness of the world.
    Must ONLY update from experienced events.
    Never queries world_frame.
    """
    current_place: Optional[str] = None
    last_transition: Optional[str] = None
    familiar_places: Dict[str, PlaceMemory] = field(default_factory=dict)

    def update_from_event(self, *, place: str, day: int, duration: float, affect: List[str] | None = None):
        if not place:
            return

        self.current_place = place

        pm = self.familiar_places.get(place)
        if pm is None:
            pm = PlaceMemory(visits=0, exposure=0.0, familiarity=0.0, comfort_bias=0.0, last_day_seen=day)
            self.familiar_places[place] = pm

        pm.visits += 1
        pm.exposure += float(duration)
        pm.last_day_seen = int(day)

        # Familiarity curve: fast early learning, then saturates
        # visits dominates at first; exposure helps later
        v = pm.visits
        e = pm.exposure
        fam = 1.0 - (1.0 / (1.0 + 0.35 * v + 0.08 * e))
        pm.familiarity = max(0.0, min(1.0, fam))

        # Comfort bias: ONLY from affect tokens (no inference)
        if affect:
            for a in affect:
                aa = a.strip().lower()
                if aa in {"comfort", "safe", "calm", "joy"}:
                    pm.comfort_bias += 0.05
                elif aa in {"fear", "pain", "cold", "wet", "hungry"}:
                    pm.comfort_bias -= 0.05
            pm.comfort_bias = max(-1.0, min(1.0, pm.comfort_bias))