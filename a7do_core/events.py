# a7do_core/events.py
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ExperienceEvent:
    """
    A single unit of lived experience.
    """
    kind: str                 # e.g. 'birth', 'care', 'travel', 'play'
    day: int
    place: str
    duration: float           # simulated duration (arbitrary units)

    # Observer-supplied tags only
    # Example:
    # {
    #   "object": ["ball"],
    #   "colour": ["red"],
    #   "affect": ["joy"]
    # }
    tags: Dict[str, List[str]]