# a7do_core/internal_log.py
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SleepInternalLog:
    """
    Records what replayed and whether it was internally coherent.
    """
    replayed_tags: List[str] = field(default_factory=list)

    # tag -> outcome ('stable', 'partial', 'conflict')
    coherence: Dict[str, str] = field(default_factory=dict)