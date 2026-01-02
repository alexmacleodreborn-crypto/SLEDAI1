# a7do/events.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExperienceEvent:
    """A single grounded experience."""
    place_id: str
    room: str = "unknown"
    agent: str = "Environment"
    action: str = "occurred"
    obj: Optional[str] = None

    # What is physically true in this moment (Observer truth)
    presence: List[str] = field(default_factory=list)     # people present
    pets: List[str] = field(default_factory=list)         # pets present

    # Sensory bundles (do not imply meaning; just channels)
    sound: Dict[str, Any] = field(default_factory=dict)
    smell: Dict[str, Any] = field(default_factory=dict)
    touch: Dict[str, Any] = field(default_factory=dict)
    vision: Dict[str, Any] = field(default_factory=dict)
    motor: Dict[str, Any] = field(default_factory=dict)

    # Spoken tokens: treated as raw sound-pattern tokens (no meaning yet)
    sounds_spoken: List[str] = field(default_factory=list)

    # Emphasis tokens (e.g. BALL) used for early language reinforcement
    emphasis: List[str] = field(default_factory=list)

    # Optional: body snapshot at the moment (for logs)
    body: Dict[str, Any] = field(default_factory=dict)

    # Movement
    movement: Dict[str, Any] = field(default_factory=dict)  # {"from":..., "to":...}

    def summary(self) -> str:
        who = ", ".join([p for p in self.presence if p]) or "—"
        pet = ", ".join([p for p in self.pets if p]) or "—"
        what = f"{self.agent} {self.action}" + (f" {self.obj}" if self.obj else "")
        return f"{self.place_id}/{self.room} | people={who} | pets={pet} | {what}"