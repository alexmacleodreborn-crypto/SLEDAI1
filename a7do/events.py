from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ExperienceEvent:
    day: int
    index: int
    kind: str          # birth, care, travel, sleep
    place: str         # hospital, home, bedroom
    people_present: List[str] = field(default_factory=list)

    movement: Optional[Dict] = None
    transport: Optional[Dict] = None
    sensory: Dict[str, List[str]] = field(default_factory=dict)

    notes: str = ""