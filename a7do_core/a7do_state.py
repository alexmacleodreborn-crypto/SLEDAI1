from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class A7DOState:
    """
    Embodied perspective slice (what A7DO can 'be in' at the moment).
    """
    current_location: Optional[str]
    somatic_signals: Dict[str, float]