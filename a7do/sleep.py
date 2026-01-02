#a7do/sleep.py

from collections import defaultdict
from typing import Dict, Any, List

class SleepEngine:
    def replay(self, events: List[Any]) -> Dict[str, Any]:
        recent = events[-12:]
        edges = defaultdict(int)

        for ev in recent:
            a = f"agent:{ev.agent}"
            p = f"place:{ev.place_id}"
            r = f"room:{ev.room}"
            edges[(a, p)] += 1
            edges[(a, r)] += 1
            edges[(p, r)] += 1
            if ev.obj:
                o = f"obj:{ev.obj}"
                edges[(a, o)] += 1
                edges[(o, p)] += 1
            for pr in getattr(ev, "presence", []) or []:
                edges[(a, f"present:{pr}")] += 1

        top = sorted(edges.items(), key=lambda kv: kv[1], reverse=True)[:20]
        return {
            "replayed_count": len(recent),
            "top_edges": [{"a": k[0], "b": k[1], "w": v} for k, v in top],
            "note": "Replay reinforces co-occurrence only."
        }