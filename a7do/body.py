from dataclasses import dataclass

@dataclass
class BiologicalState:
    hunger: float = 0.5
    stomach_hurt: float = 0.0
    fatigue: float = 0.2

    def clamp(self):
        self.hunger = max(0.0, min(1.0, self.hunger))
        self.stomach_hurt = max(0.0, min(1.0, self.stomach_hurt))
        self.fatigue = max(0.0, min(1.0, self.fatigue))

    def tick_awake(self):
        self.hunger += 0.08
        self.fatigue += 0.06
        if self.hunger > 0.8:
            self.stomach_hurt += 0.05
        self.clamp()

    def feed(self):
        self.hunger -= 0.35
        self.stomach_hurt -= 0.10
        self.clamp()

    def rest(self):
        self.fatigue -= 0.40
        self.clamp()

    def cry_level(self) -> float:
        return max(self.hunger, self.stomach_hurt, self.fatigue)

    def snapshot(self):
        return {
            "hunger": round(self.hunger, 2),
            "stomach_hurt": round(self.stomach_hurt, 2),
            "fatigue": round(self.fatigue, 2),
            "cry_level": round(self.cry_level(), 2),
        }