# a7do_core/a7mind.py

from typing import List

from a7do_core.familiarity import FamiliarityMemory


class A7DOMind:
    """
    Core pre-symbolic mind.
    Receives sensory packets, tracks familiarity, sleeps.
    """

    def __init__(self):
        self.sensory_memory: List = []
        self.familiarity = FamiliarityMemory()

    def process_sensory_packet(self, packet):
        """
        Receive a sensory packet from the world bridge.
        """
        # Observe sensory patterns (wake phase)
        for modality, values in packet.sensory.items():
            for v in values:
                self.familiarity.observe(modality, v)

        self.sensory_memory.append(packet)

    def snapshot(self):
        """
        Internal debug snapshot.
        """
        return {
            "sensory_memory_count": len(self.sensory_memory),
            "familiarity": self.familiarity.snapshot(),
        }