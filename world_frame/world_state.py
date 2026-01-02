from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class WorldState:
    current_day: int = 0
    current_place_id: Optional[str] = None

    # Ground truth registries
    places: Dict[str, dict] = field(default_factory=dict)
    entities: Dict[str, dict] = field(default_factory=dict)
    objects: Dict[str, dict] = field(default_factory=dict)

    # Movement + presence logs
    presence: Dict[str, str] = field(default_factory=dict)

    def snapshot(self):
        return {
            "day": self.current_day,
            "place": self.current_place_id,
            "places": list(self.places.keys()),
            "entities": list(self.entities.keys()),
            "objects": list(self.objects.keys()),
            "presence": self.presence.copy(),
        }