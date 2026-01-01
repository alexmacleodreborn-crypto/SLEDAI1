from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class ExperienceEvent:
    place_id: str
    room: str
    agent: str
    action: str
    obj: Optional[str] = None

    narrator: Optional[str] = None
    emphasis: List[str] = field(default_factory=list)

    sound: Dict[str, str] = field(default_factory=dict)
    smell: Dict[str, str] = field(default_factory=dict)
    touch: Dict[str, str] = field(default_factory=dict)
    motor: Dict[str, str] = field(default_factory=dict)

    # movement
    to_place_id: Optional[str] = None
    to_room: Optional[str] = None
    pos_xyz: Optional[Tuple[float, float, float]] = None

    # presence (social continuity without coupling)
    presence: List[str] = field(default_factory=list)

    # touch vector (somatic scaffold)
    touch_vector: Dict[str, float] = field(default_factory=dict)  # {"region":..., "pressure":..., "temp":..., "duration_s":...}

    # body snapshot
    body: Dict[str, float] = field(default_factory=dict)

    # transaction
    transaction: Dict[str, str] = field(default_factory=dict)

    def prompt(self) -> str:
        parts = [self.agent, self.action]
        if self.obj:
            parts.append(self.obj)
        if self.emphasis:
            parts.append(f"(emphasis: {', '.join(self.emphasis)})")
        return " ".join(parts)