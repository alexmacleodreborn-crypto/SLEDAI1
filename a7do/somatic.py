from dataclasses import dataclass, field
from typing import Dict

REGIONS = ["head", "torso", "left_arm", "right_arm", "left_leg", "right_leg", "hands", "feet"]

@dataclass
class SomaticRegion:
    pressure: float = 0.0
    temperature: float = 0.0   # signed: -cold .. +warm
    pain: float = 0.0
    contact_s: float = 0.0

@dataclass
class SomaticState:
    regions: Dict[str, SomaticRegion] = field(default_factory=lambda: {r: SomaticRegion() for r in REGIONS})

    def apply_touch(self, region: str, pressure: float, temperature: float, duration_s: float):
        if region not in self.regions:
            return
        r = self.regions[region]
        r.pressure = max(0.0, min(1.0, pressure))
        r.temperature = max(-1.0, min(1.0, temperature))
        r.contact_s = max(0.0, duration_s)

        # pain heuristic
        pain = 0.0
        if r.pressure > 0.8:
            pain += (r.pressure - 0.8) * 2.5
        if abs(r.temperature) > 0.7:
            pain += (abs(r.temperature) - 0.7) * 2.0
        r.pain = max(0.0, min(1.0, pain))

    def snapshot(self):
        return {k: {"pressure": v.pressure, "temp": v.temperature, "pain": v.pain, "contact_s": v.contact_s} for k, v in self.regions.items()}