# a7do_core/a7mind.py

from dataclasses import dataclass
from typing import List, Dict, Any

from a7do_core.sleep import SleepEngine


@dataclass
class SensoryMemory:
    """
    A raw stored sensory experience.
    No meaning. No language. No inference.
    """
    place: str
    sensory: Dict[str, List[str]]
    body: Dict[str, Any]
    tags: List[str]
    time: float


class A7Mind:
    """
    Minimal embodied mind for A7DO.

    This mind:
    - receives sensory packets
    - stores them
    - sleeps (replay + stabilization)
    - exposes safe snapshots

    It does NOT:
    - reason
    - speak
    - label
    - infer
    """

    def __init__(self):
        self.birthed: bool = False
        self.current_place: str = "Unknown"

        self.sensory_memories: List[SensoryMemory] = []
        self.sleep_engine = SleepEngine()

    # ---------------------------------------------------------
    # Perception
    # ---------------------------------------------------------

    def receive_sensory_packet(self, packet):
        """
        Receive a sensory packet from the world bridge.
        """
        self.birthed = True
        self.current_place = packet.place

        self.sensory_memories.append(
            SensoryMemory(
                place=packet.place,
                sensory=packet.sensory,
                body=packet.body,
                tags=packet.tags,
                time=packet.time,
            )
        )

    # ---------------------------------------------------------
    # Sleep
    # ---------------------------------------------------------

    def sleep(self):
        """
        Enter sleep phase.
        Replays and stabilizes recent experience.
        """
        self.sleep_engine.sleep(self.sensory_memories)

    # ---------------------------------------------------------
    # Observer-safe snapshot
    # ---------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        """
        Safe state exposure for UI / Observer.
        """
        return {
            "birthed": self.birthed,
            "current_place": self.current_place,
            "sensory_memory_count": len(self.sensory_memories),
            "recent_tags": (
                self.sensory_memories[-1].tags
                if self.sensory_memories
                else []
            ),
            "sleep": self.sleep_engine.snapshot(),
        }