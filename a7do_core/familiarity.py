# a7do_core/familiarity.py

from collections import defaultdict
from typing import Tuple, Dict


class FamiliarityMemory:
    """
    Tracks familiarity of sensory patterns.
    Familiarity is prediction confidence, not liking.
    """

    def __init__(self):
        self._scores = defaultdict(float)

    def _key(self, modality: str, value: str) -> Tuple[str, str]:
        return (modality.strip().lower(), value.strip().lower())

    def observe(self, modality: str, value: str, delta: float = 0.02):
        """
        Increase familiarity slightly during waking experience.
        """
        key = self._key(modality, value)
        self._scores[key] = min(1.0, self._scores[key] + delta)

    def reinforce(self, modality: str, value: str, delta: float = 0.01):
        """
        Reinforce familiarity during sleep replay.
        """
        key = self._key(modality, value)
        self._scores[key] = min(1.0, self._scores[key] + delta)

    def get(self, modality: str, value: str) -> float:
        return self._scores.get(self._key(modality, value), 0.0)

    def snapshot(self) -> Dict[str, float]:
        """
        Debug snapshot of known familiar patterns.
        """
        return {
            f"{k[0]}:{k[1]}": round(v, 3)
            for k, v in self._scores.items()
            if v >= 0.05
        }