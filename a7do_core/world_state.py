# a7do_core/world_state.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class WorldState:
    # Temporal
    day: int = 0
    time: float = 0.0  # simulated time units

    # Spatial
    location: Optional[str] = None

    # Presence
    people_present: List[str] = field(default_factory=list)
    objects_present: List[str] = field(default_factory=list)

    # Body & somatic signals (raw accumulation only)
    body_state: Dict[str, float] = field(default_factory=dict)

    # History (event kinds only, no interpretation)
    event_history: List[str] = field(default_factory=list)

    # Safety
    frozen: bool = False  # MUST be true during sleep replay