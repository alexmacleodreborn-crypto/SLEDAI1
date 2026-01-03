# a7do_core/sleep.py

class SleepProcessor:
    """
    Handles sleep consolidation.
    """

    def __init__(self, mind):
        self.mind = mind

    def sleep_cycle(self):
        """
        Replay recent sensory experiences to stabilise familiarity.
        """
        if not self.mind.sensory_memory:
            return

        recent_packets = self.mind.sensory_memory[-50:]

        for packet in recent_packets:
            for modality, values in packet.sensory.items():
                for v in values:
                    self.mind.familiarity.reinforce(modality, v)