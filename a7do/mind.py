from typing import Dict, Any, List
from collections import defaultdict
from a7do.sleep import SleepEngine

class A7DOMind:
    """
    Non-aware learner.
    - Stores events
    - Updates lexicon exposure counts
    - Builds association strengths
    - Observer trace shows formation
    """
    def __init__(self, schedule, world_map, profiles):
        self.schedule = schedule
        self.world_map = world_map
        self.profiles = profiles

        self.memory: List[Any] = []
        self.lexicon: Dict[str, int] = {}
        self.edges = defaultdict(int)  # (nodeA,nodeB)->weight

        self.sleep_engine = SleepEngine()

        self.trace: List[Dict[str, Any]] = []
        self.last = None
        self.last_sleep = None
        self.last_coherence = None

    def _inc(self, token: str):
        t = (token or "").strip().lower()
        if not t:
            return
        self.lexicon[t] = self.lexicon.get(t, 0) + 1

    def coherence_check(self, ev) -> Dict[str, Any]:
        issues = []
        # building exists
        if ev.building not in self.world_map.buildings:
            issues.append(f"unknown_building:{ev.building}")
        else:
            b = self.world_map.buildings[ev.building]
            if b.kind == "house" and ev.room not in b.rooms:
                issues.append(f"unknown_room:{ev.room}")

        # parents required
        if not self.profiles.has_parents():
            issues.append("parents_missing")

        # agent must exist in profiles
        agent_ok = (ev.agent in self.profiles.people) or (ev.agent in self.profiles.animals)
        if not agent_ok:
            issues.append(f"unknown_agent:{ev.agent}")

        # object must exist if specified
        if ev.obj and (ev.obj not in self.profiles.objects) and (ev.obj not in self.profiles.animals):
            issues.append(f"unknown_object:{ev.obj}")

        score = 1.0 if not issues else max(0.0, 1.0 - 0.25 * len(issues))
        return {"score": round(score, 2), "issues": issues}

    def ingest(self, ev) -> Dict[str, Any]:
        coh = self.coherence_check(ev)
        self.last_coherence = coh

        if coh["score"] <= 0.25:
            self.last = "blocked"
            self.trace.append({"phase": "blocked", "prompt": ev.prompt(), "coherence": coh})
            return {"ok": False, "blocked": True, "coherence": coh}

        # movement inference via room transition
        if ev.to_room:
            frm = self.schedule.spatial.room
            self.schedule.spatial.room = ev.to_room
            self.trace.append({"phase": "movement", "from": frm, "to": ev.to_room})

        if ev.pos_xy:
            self.schedule.spatial.pos_xy = ev.pos_xy

        if ev.motor.get("type") in ("crawl", "walk"):
            self.schedule.spatial.locomotion = ev.motor.get("type")

        # memory store
        self.memory.append(ev)

        # lexicon exposure: place, agent, action, object, emphasis, sensory labels
        self._inc(ev.room)
        self._inc(ev.agent)
        self._inc(ev.action)
        if ev.obj:
            self._inc(ev.obj)
        for w in (ev.emphasis or []):
            self._inc(w)
        if ev.sound:
            self._inc("sound")
            self._inc(ev.sound.get("pattern", ""))
        if ev.smell:
            self._inc("smell")
            self._inc(ev.smell.get("pattern", ""))
        if ev.motor:
            self._inc("motor")
            self._inc(ev.motor.get("type", ""))

        # edges reinforcement (observer-only)
        a = f"agent:{ev.agent}"
        r = f"room:{ev.room}"
        self.edges[(a, r)] += 1
        if ev.obj:
            o = f"obj:{ev.obj}"
            self.edges[(o, r)] += 1
            self.edges[(a, o)] += 1
        if ev.to_room:
            tr = f"room:{ev.to_room}"
            self.edges[(r, tr)] += 1

        self.last = f"experienced: {ev.room}"
        self.trace.append({
            "phase": "experience",
            "prompt": ev.prompt(),
            "event": {
                "building": ev.building,
                "room": ev.room,
                "to_room": ev.to_room,
                "agent": ev.agent,
                "action": ev.action,
                "object": ev.obj,
                "emphasis": ev.emphasis,
                "sound": ev.sound,
                "smell": ev.smell,
                "motor": ev.motor,
                "pos_xy": ev.pos_xy,
                "body": ev.body,
            },
            "coherence": coh
        })
        return {"ok": True, "coherence": coh}

    def sleep(self) -> Dict[str, Any]:
        self.last = "sleep"
        rep = self.sleep_engine.replay(self.memory)
        self.last_sleep = rep
        self.trace.append({"phase": "sleep", "report": rep})
        return rep