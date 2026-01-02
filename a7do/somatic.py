# a7do/somatic.py

class SomaticState:
    """
    Embodied somatic state for A7DO.
    Represents where sensations are felt on the body.
    """

    def __init__(self):
        # Hierarchical body zones
        self.zones = {
            "head": 0.0,
            "face": 0.0,
            "neck": 0.0,
            "chest": 0.0,
            "back": 0.0,
            "abdomen": 0.0,
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_hand": 0.0,
            "right_hand": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
            "left_foot": 0.0,
            "right_foot": 0.0,
        }

    def apply_touch(self, zone: str, intensity: float = 0.2):
        """Register touch or pressure at a body zone."""
        if zone in self.zones:
            self.zones[zone] = min(1.0, self.zones[zone] + intensity)

    def apply_pain(self, zone: str, intensity: float = 0.4):
        """Register discomfort or pain."""
        if zone in self.zones:
            self.zones[zone] = min(1.0, self.zones[zone] + intensity)

    def decay(self):
        """Natural fading of sensations."""
        for z in self.zones:
            self.zones[z] = max(0.0, self.zones[z] - 0.05)

    def snapshot(self) -> dict:
        """Return active sensations only."""
        return {z: round(v, 3) for z, v in self.zones.items() if v > 0.0}


# Backward / semantic alias
SomaticMap = SomaticState