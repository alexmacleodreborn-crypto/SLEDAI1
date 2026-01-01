from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class ExperienceEvent:
    place_id: str
    room: str
    agent: str
    action: str
    obj: Optional[str] = None

    # “story text” is not given to A7DO, but Observer can see it
    narrator: Optional[str] = None

    # emphasis tokens (e.g., BALL)
    emphasis: List[str] = field(default_factory=list)

    # sensory channels
    sound: Dict[str, str] = field(default_factory=dict)
    smell: Dict[str, str] = field(default_factory=dict)
    touch: Dict[str, str] = field(default_factory=dict)
    motor: Dict[str, str] = field(default_factory=dict)

    # movement inference
    to_place_id: Optional[str] = None
    to_room: Optional[str] = None
    pos_xyz: Optional[Tuple[float, float, float]] = None

    # body snapshot
    body: Dict[str, float] = field(default_factory=dict)

    # transaction recording (for social contacts)
    transaction: Dict[str, str] = field(default_factory=dict)  # { "target": "A7DO", "outcome": "cried" }

    def prompt(self) -> str:
        parts = [self.agent, self.action]
        if self.obj:
            parts.append(self.obj)
        if self.emphasis:
            parts.append(f"(emphasis: {', '.join(self.emphasis)})")
        return " ".join(parts)