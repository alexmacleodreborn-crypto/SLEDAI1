from collections import defaultdict
from typing import Dict, Any

class SleepEngine:
    """
    Replay + reinforcement stats only (observer-visible).
    """
    def replay(self, memory_events) -> Dict[str, Any]:
        recent = memory_events[-10:]
        edge = defaultdict(int)

        for ev in recent:
            r = f"room:{ev.room}"
            a = f"agent:{ev.agent}"
            edge[(a, r)] += 1
            if ev.obj:
                o = f"obj:{ev.obj}"
                edge[(o, r)] += 1
                edge[(a, o)] += 1
            if ev.to_room:
                tr = f"room:{ev.to_room}"
                edge[(r, tr)] += 1

        top = sorted(edge.items(), key=lambda x: x[1], reverse=True)[:15]
        top_edges = [{"a": k[0], "b": k[1], "w": v} for k, v in top]

        return {
            "replayed_count": len(recent),
            "top_edges": top_edges,
            "note": "No abstraction. Reinforcement stats only."
        }