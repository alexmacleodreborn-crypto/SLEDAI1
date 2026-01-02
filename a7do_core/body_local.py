from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ReflexRecord:
    stimulus: str              # e.g. "eye_itch", "wet", "cold"
    action: str                # e.g. "rub_eye", "cry", "kick"
    relief: float              # positive relief score
    count: int = 0


@dataclass
class LocalBody:
    """
    Local (non-cognitive) body loops:
    - learns stimulus -> action -> relief
    - bypasses Sandy gates entirely
    - no words, no concepts, no meaning
    """
    reflexes: Dict[str, ReflexRecord] = field(default_factory=dict)
    last_action: Optional[str] = None
    action_history: List[str] = field(default_factory=list)

    def record_relief(self, stimulus: str, action: str, relief: float):
        key = f"{stimulus}::{action}"
        rec = self.reflexes.get(key)
        if rec is None:
            rec = ReflexRecord(stimulus=stimulus, action=action, relief=float(relief), count=1)
            self.reflexes[key] = rec
        else:
            rec.relief = (rec.relief * rec.count + float(relief)) / (rec.count + 1)
            rec.count += 1

    def choose_action(self, active_stimuli: List[str]) -> Optional[str]:
        """
        Pick the best-known reflex for any active stimulus.
        Returns an action string, or None.
        """
        best: Tuple[float, Optional[str]] = (-1e9, None)
        for stim in active_stimuli:
            for rec in self.reflexes.values():
                if rec.stimulus == stim and rec.relief > best[0]:
                    best = (rec.relief, rec.action)

        return best[1]

    def enact(self, action: str):
        self.last_action = action
        self.action_history.append(action)