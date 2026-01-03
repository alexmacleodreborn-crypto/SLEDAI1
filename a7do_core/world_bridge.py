# a7do_core/world_bridge.py

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class SensoryPacket:
    place: str
    sensory: Dict[str, List[str]]
    body: Dict[str, Any]
    tags: List[str]
    time: float


class WorldToA7DOBridge:
    """
    Converts WorldEvents into sensory packets.
    """

    def __init__(self):
        self.last_world_time: float = 0.0

    def translate_event(self, world_event) -> Optional[SensoryPacket]:
        sensory = world_event.sensory or {}
        body = {}
        tags = list(world_event.tags)

        if not sensory:
            return None

        return SensoryPacket(
            place=world_event.place,
            sensory=sensory,
            body=body,
            tags=tags,
            time=world_event.time,
        )

    def pull_new_packets(self, world_state) -> List[SensoryPacket]:
        packets = []

        for ev in world_state.events:
            if ev.time >= self.last_world_time:
                pkt = self.translate_event(ev)
                if pkt:
                    packets.append(pkt)

        self.last_world_time = world_state.time
        return packets