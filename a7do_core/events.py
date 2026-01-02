from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ExperienceEvent:
    """
    A single unit of lived experience (observer-supplied).
    No meaning is inferred from these fields.
    """
    kind: str                 # e.g. 'birth', 'care', 'travel', 'play', 'experience'
    day: int
    place: str
    duration: float           # simulated duration (arbitrary units)
    tags: Dict[str, List[str]]  # observer-provided labels (some may be sensory)