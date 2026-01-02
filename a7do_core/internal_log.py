from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SleepInternalLog:
    """
    Sleep log: validates stability; stores pre-language echoes only.
    """
    replayed_tags: List[str] = field(default_factory=list)
    coherence: Dict[str, str] = field(default_factory=dict)

    contrast_summary: Dict[str, List[str]] = field(default_factory=lambda: {
        "comfort": [],
        "discomfort": [],
    })

    motor_echoes: List[str] = field(default_factory=list)
    vocalisations: List[str] = field(default_factory=list)

    # New: self-generated motor-sound patterns (proto syllables)
    self_generated_sounds: List[str] = field(default_factory=list)