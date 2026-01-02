# a7do/somatic.py

class SomaticState:
    """
    Somatic (body surface) state. Maps where sensation occurs.
    """

    def __init__(self):
        self.zones = {
            "head": 0.0, "face": 0.0, "neck": 0.0,
            "chest": 0.0, "back": 0.0, "abdomen": 0.0,
            "left_arm": 0.0, "right_arm": 0.0,
            "left_hand": 0.0, "right_hand": 0.0,
            "left_leg": 0.0, "right_leg": 0.0,
            "left_foot": 0.0, "right_foot": 0.0,
        }

    def apply_touch(self, zone: str, intensity: float = 0.2):
        if zone in self.zones:
            self.zones[zone] = min(1.0, self.zones[zone] + intensity)

    def apply_pain(self, zone: str, intensity: float = 0.4):
        if zone in self.zones:
            self.zones[zone] = min(1.0, self.zones[zone] + intensity)

    def decay(self):
        for k in self.zones:
            self.zones[k] = max(0.0, self.zones[k] - 0.05)

    def snapshot(self) -> dict:
        return {k: round(v, 3) for k, v in self.zones.items() if v > 0.0}


SomaticMap = SomaticState  # compatibility alias