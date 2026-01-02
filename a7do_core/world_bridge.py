# a7do_core/world_bridge.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class SensoryPacket:
    """
    A single moment of possible perception.
    This does NOT mean A7DO understands it.
    """
    place: str
    sensory: Dict[str, List[str]]  # visual, sound, touch, smell, taste
    body: Dict[str, Any]           # limb movement, pressure, discomfort
    tags: List[str]
    time: float


class WorldToA7DOBridge:
    """
    Converts objective WorldEvents into gated sensory packets.
    """

    def __init__(self):
        self.last_world_time: float = 0.0

    def translate_event(self, world_event) -> Optional[SensoryPacket]:
        """
        Convert a WorldEvent into a SensoryPacket.
        Return None if nothing perceptible occurred.
        """

        sensory: Dict[str, List[str]] = {}
        body: Dict[str, Any] = {}
        tags: List[str] = []

        # --- Basic place awareness ---
        place = getattr(world_event, "place", "Unknown")

        # --- Sensory extraction ---
        if hasattr(world_event, "sensory"):
            sensory = world_event.sensory

        # --- Fallback from description ---
        description = getattr(world_event, "description", "").lower()

        if "cry" in description:
            sensory.setdefault("sound", []).append("crying")
            body["distress"] = True
            tags.append("distress")

        if "cold" in description:
            sensory.setdefault("touch", []).append("cold")
            body["temperature"] = "cold"
            tags.append("temperature")

        if "light" in description:
            sensory.setdefault("visual", []).append("bright light")
            tags.append("visual")

        if not sensory and not body:
            # Nothing perceptible
            return None

        return SensoryPacket(
            place=place,
            sensory=sensory,
            body=body,
            tags=tags,
            time=getattr(world_event, "time", 0.0),
        )

    def pull_new_packets(self, world_state) -> List[SensoryPacket]:
        """
        Pull all new world events since last check
        and convert them into sensory packets.
        """

        packets: List[SensoryPacket] = []

        for ev in world_state.events:
            if ev.time > self.last_world_time:
                pkt = self.translate_event(ev)
                if pkt:
                    packets.append(pkt)

        self.last_world_time = world_state.time
        return packets