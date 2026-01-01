from dataclasses import dataclass

@dataclass
class BiologicalState:
    hunger: float = 0.5          # 0..1
    stomach_hurt: float = 0.0    # 0..1
    fatigue: float = 0.2         # 0..1

    def clamp(self):
        self.hunger = max(0.0, min(1.0, self.hunger))
        self.stomach_hurt = max(0.0, min(1.0, self.stomach_hurt))
        self.fatigue = max(0.0, min(1.0, self.fatigue))

    def tick_awake(self):
        # awake makes hunger and fatigue creep up
        self.hunger += 0.08
        self.fatigue += 0.06
        # stomach discomfort may rise if very hungry
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
        # crying is a signal, not intention
        return max(self.hunger, self.stomach_hurt, self.fatigue)

    def snapshot(self):
        return {
            "hunger": round(self.hunger, 2),
            "stomach_hurt": round(self.stomach_hurt, 2),
            "fatigue": round(self.fatigue, 2),
            "cry_level": round(self.cry_level(), 2),
        }