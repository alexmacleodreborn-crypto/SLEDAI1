from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class ExperienceEvent:
    # location grounding
    building: str
    room: str

    # social grounding
    agent: str
    action: str
    obj: Optional[str] = None

    # reinforcement
    emphasis: List[str] = field(default_factory=list)

    # sensory channels
    sound: Dict[str, str] = field(default_factory=dict)
    smell: Dict[str, str] = field(default_factory=dict)
    motor: Dict[str, str] = field(default_factory=dict)

    # movement inference
    to_room: Optional[str] = None
    pos_xy: Optional[Tuple[float, float]] = None

    # body snapshot at moment (for observer trace)
    body: Dict[str, float] = field(default_factory=dict)

    def prompt(self) -> str:
        parts = [self.agent, self.action]
        if self.obj:
            parts.append(self.obj)
        if self.emphasis:
            parts.append(f"(emphasis: {', '.join(self.emphasis)})")
        return " ".join(parts)