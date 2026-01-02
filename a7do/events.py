# a7do/events.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ExperienceEvent:
    day: int
    index: int
    place: str

    people_present: List[str] = field(default_factory=list)
    pets_present: List[str] = field(default_factory=list)

    sensory: Dict[str, str] = field(default_factory=dict)
    sounds: List[str] = field(default_factory=list)

    movement: Optional[Dict[str, str]] = None
    body_effects: Dict[str, str] = field(default_factory=dict)

    note: str = ""  # observer/debug only