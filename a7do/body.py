# a7do/body.py

class BodyState:
    """
    Minimal embodied state for A7DO.
    This is NOT cognition — it is physiology.
    """

    def __init__(self):
        self.hunger = 0.3
        self.fatigue = 0.2
        self.discomfort = 0.1
        self.cry = 0.0

    def update(self):
        """Drift physiology over time."""
        self.hunger = min(1.0, self.hunger + 0.02)
        self.fatigue = min(1.0, self.fatigue + 0.015)
        self.discomfort = min(1.0, self.discomfort + 0.01)
        self._recalc_cry()

    def soothe(self, amount=0.2):
        self.discomfort = max(0.0, self.discomfort - amount)
        self.cry = max(0.0, self.cry - amount)

    def feed(self):
        self.hunger = max(0.0, self.hunger - 0.4)
        self._recalc_cry()

    def sleep(self):
        self.fatigue = max(0.0, self.fatigue - 0.6)
        self._recalc_cry()

    def _recalc_cry(self):
        self.cry = min(
            1.0,
            0.5 * self.hunger + 0.3 * self.fatigue + 0.4 * self.discomfort,
        )

    def cry_level(self) -> float:
        return round(self.cry, 3)

    def snapshot(self) -> dict:
        return {
            "hunger": round(self.hunger, 3),
            "fatigue": round(self.fatigue, 3),
            "discomfort": round(self.discomfort, 3),
            "cry": round(self.cry, 3),
        }