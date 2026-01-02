# a7do/somatic.py

class SomaticMap:
    """
    Maps bodily sensation locations.
    This is a spatial body schema, not cognition.
    """

    def __init__(self):
        # Simple hierarchical body map
        self.zones = {
            "head": 0.0,
            "face": 0.0,
            "chest": 0.0,
            "back": 0.0,
            "left_arm": 0.0,
            "right_arm": 0.0,
            "left_hand": 0.0,
            "right_hand": 0.0,
            "abdomen": 0.0,
            "left_leg": 0.0,
            "right_leg": 0.0,
            "left_foot": 0.0,
            "right_foot": 0.0,
        }

    def apply_touch(self, zone: str, intensity: float = 0.2):
        """Register touch/pressure at a body zone."""
        if zone in self.zones:
            self.zones[zone] = min(1.0, self.zones[zone] + intensity)

    def decay(self):
        """Natural fading of sensation."""
        for z in self.zones:
            self.zones[z] = max(0.0, self.zones[z] - 0.05)

    def snapshot(self) -> dict:
        """Return active sensations only."""
        return {z: round(v, 3) for z, v in self.zones.items() if v > 0.0}