from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class WorldState:
    # Temporal
    day: int = 0
    time: float = 0.0

    # Spatial
    location: Optional[str] = None

    # History (kinds only)
    event_history: List[str] = field(default_factory=list)

    # Raw somatic accumulation by channel (not interpretation)
    # e.g. {"sound": 0.3, "touch": 0.2, ...}
    body_state: Dict[str, float] = field(default_factory=dict)

    # System guard: frozen during sleep replay (no mutation permitted)
    frozen: bool = False