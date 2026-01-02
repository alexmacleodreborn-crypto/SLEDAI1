from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BotState:
    name: str
    location: str
    last_seen_day: int = 0
    last_seen_event: int = 0


@dataclass
class WorldState:
    # Time
    current_day: int = 0
    current_event_index: int = 0

    # A7DO physical state
    a7do_location: str = "hospital"
    a7do_posture: str = "lying"

    # Movement / transport
    last_movement: dict = field(default_factory=dict)
    last_transport: dict = field(default_factory=dict)

    # Sleep
    last_sleep_location: str = ""
    last_sleep_day: int = -1

    # Other agents
    bots: Dict[str, BotState] = field(default_factory=dict)