# a7do_core/sleep.py

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SleepTrace:
    """
    One replayed sensory moment during sleep.
    """
    place: str
    tags: List[str]
    comfort_score: float
    time: float


class SleepEngine:
    """
    Handles sleep-phase replay and stabilization.
    """

    def __init__(self):
        self.sleep_cycles: int = 0
        self.traces: List[SleepTrace] = []

    def sleep(self, sensory_memories: List[Any]):
        """
        Perform one sleep cycle over recent sensory memories.
        """
        self.sleep_cycles += 1
        self.traces.clear()

        for mem in sensory_memories:
            comfort = self._score_comfort(mem)
            self.traces.append(
                SleepTrace(
                    place=mem.place,
                    tags=mem.tags,
                    comfort_score=comfort,
                    time=mem.time,
                )
            )

    def _score_comfort(self, mem) -> float:
        """
        Very simple comfort / distress heuristic.
        """
        score = 0.0

        if "distress" in mem.tags:
            score -= 1.0

        if "temperature" in mem.tags:
            if mem.body.get("temperature") == "cold":
                score -= 0.5

        if not mem.tags:
            score += 0.2  # neutral calm presence

        return score

    def snapshot(self) -> Dict[str, Any]:
        """
        Observer-safe view of sleep state.
        """
        return {
            "sleep_cycles": self.sleep_cycles,
            "trace_count": len(self.traces),
            "avg_comfort": (
                round(
                    sum(t.comfort_score for t in self.traces)
                    / len(self.traces),
                    3,
                )
                if self.traces
                else 0.0
            ),
        }