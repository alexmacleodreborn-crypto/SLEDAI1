# a7do_core/a7do_state.py
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class A7DOState:
    """
    Embodied perspective of A7DO at a moment in time.
    """
    current_location: Optional[str]
    somatic_signals: Dict[str, float]