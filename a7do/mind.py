from typing import Dict, Any, List
from collections import defaultdict
from a7do.sleep import SleepEngine
from a7do.somatic import SomaticState

class A7DOMind:
    def __init__(self, world_map, profiles, schedule):
        self.world = world_map
        self.profiles = profiles
        self.schedule = schedule

        self.memory: List[Any] = []
        self.lexicon: Dict[str, int] = {}
        self.edges = defaultdict(int)
        self.trace: List[Dict[str, Any]] = []

        self.sleep_engine = SleepEngine()
        self.somatic = SomaticState()

        self.last_coherence = None
        self.last_sleep = None
        self.last_action = None

    def _inc(self, token: str):
        t = (token or "").strip().lower()
        if not t:
            return
        self.lexicon[t] = self.lexicon.get(t, 0) + 1

    def coherence_check(self, ev) -> Dict[str, Any]:
        issues = []

        if ev.place_id not in self.world.places:
            issues.append(f"unknown_place:{ev.place_id}")
        else:
            place = self.world.places[ev.place_id]
            if place.kind in ("hospital", "house") and ev.room and ev.room not in place.rooms:
                issues.append(f"unknown_room:{ev.room}")

        agent_ok = (ev.agent == "A7DO") or (ev.agent in self.profiles.people) or (ev.agent in self.profiles.animals) or (ev.agent in ("Nurse", "Street"))
        if not agent_ok:
            issues.append(f"unknown_agent:{ev.agent}")

        score = 1.0 if not issues else max(0.0, 1.0 - 0.2 * len(issues))
        return {"score": round(score, 2), "issues": issues}

    def ingest(self, ev) -> Dict[str, Any]:
        coh = self.coherence_check(ev)
        self.last_coherence = coh

        if coh["score"] <= 0.2:
            self.last_action = "blocked"
            self.trace.append({"phase": "blocked", "prompt": ev.prompt(), "coherence": coh})
            return {"ok": False, "blocked": True, "coherence": coh}

        # movement
        if ev.to_place_id:
            self.schedule.spatial.place_id = ev.to_place_id
        if ev.to_room:
            self.schedule.spatial.room = ev.to_room
        if ev.pos_xyz:
            self.schedule.spatial.pos_xyz = ev.pos_xyz
        if ev.motor.get("type"):
            self.schedule.spatial.locomotion = ev.motor.get("type")

        # somatic touch
        tv = getattr(ev, "touch_vector", None) or {}
        if tv and "region" in tv:
            self.somatic.apply_touch(
                region=str(tv.get("region")),
                pressure=float(tv.get("pressure", 0.0)),
                temperature=float(tv.get("temp", 0.0)),
                duration_s=float(tv.get("duration_s", 0.0)),
            )

        # store memory
        self.memory.append(ev)

        # lexicon
        for token in [ev.place_id, ev.room, ev.agent, ev.action, ev.obj]:
            if token:
                self._inc(str(token))
        for w in ev.emphasis:
            self._inc(w)

        # edges
        a = f"agent:{ev.agent}"
        p = f"place:{ev.place_id}"
        r = f"room:{ev.room}"
        self.edges[(a, p)] += 1
        self.edges[(a, r)] += 1
        self.edges[(p, r)] += 1
        if ev.obj:
            o = f"obj:{ev.obj}"
            self.edges[(a, o)] += 1
            self.edges[(o, p)] += 1
        for pr in ev.presence:
            self.edges[(a, f"present:{pr}")] += 1

        # transaction logging
        if ev.transaction and ev.transaction.get("target") == "A7DO":
            outcome = ev.transaction.get("outcome", "calm")
            self.profiles.set_interaction(ev.agent, outcome=outcome, day=self.schedule.day)

        self.last_action = f"experience:{ev.place_id}/{ev.room}"
        self.trace.append({
            "phase": "experience",
            "prompt": ev.prompt(),
            "event": {
                "place_id": ev.place_id,
                "room": ev.room,
                "agent": ev.agent,
                "action": ev.action,
                "obj": ev.obj,
                "presence": ev.presence,
                "touch_vector": ev.touch_vector,
                "coherence": coh,
                "narrator": ev.narrator
            },
            "coherence": coh
        })
        return {"ok": True, "coherence": coh}

    def sleep(self) -> Dict[str, Any]:
        rep = self.sleep_engine.replay(self.memory)
        self.last_sleep = rep
        self.trace.append({"phase": "sleep", "report": rep})
        self.last_action = "sleep"
        return rep