# a7do/body.py

class BiologicalState:
    """
    Embodied physiological state for A7DO.
    This is NOT cognition — it is biology/needs.
    """

    def __init__(self):
        self.hunger = 0.30
        self.fatigue = 0.20
        self.discomfort = 0.10
        self.cry = 0.00

    def update(self):
        """Natural drift while awake."""
        self.hunger = min(1.0, self.hunger + 0.02)
        self.fatigue = min(1.0, self.fatigue + 0.015)
        self.discomfort = min(1.0, self.discomfort + 0.01)
        self._recalc_cry()

    def soothe(self, amount=0.20):
        self.discomfort = max(0.0, self.discomfort - amount)
        self._recalc_cry()

    def feed(self):
        self.hunger = max(0.0, self.hunger - 0.40)
        self._recalc_cry()

    def sleep(self):
        self.fatigue = max(0.0, self.fatigue - 0.60)
        self._recalc_cry()

    def _recalc_cry(self):
        self.cry = min(
            1.0,
            0.5 * self.hunger +
            0.3 * self.fatigue +
            0.4 * self.discomfort
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


BodyState = BiologicalState  # compatibility alias