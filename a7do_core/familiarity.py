# a7do_core/familiarity.py

from collections import defaultdict
from typing import Tuple


class FamiliarityMemory:
    """
    Tracks how familiar sensory patterns are.
    Familiarity ≠ preference.
    """

    def __init__(self):
        self._scores = defaultdict(float)

    def _key(self, modality: str, value: str) -> Tuple[str, str]:
        return (modality, value)

    def observe(self, modality: str, value: str, delta: float = 0.02):
        key = self._key(modality, value)
        self._scores[key] = min(1.0, self._scores[key] + delta)

    def reinforce(self, modality: str, value: str, delta: float = 0.01):
        key = self._key(modality, value)
        self._scores[key] = min(1.0, self._scores[key] + delta)

    def get(self, modality: str, value: str) -> float:
        return self._scores.get(self._key(modality, value), 0.0)

    def snapshot(self):
        return {
            f"{k[0]}:{k[1]}": round(v, 3)
            for k, v in self._scores.items()
            if v > 0.05
        }