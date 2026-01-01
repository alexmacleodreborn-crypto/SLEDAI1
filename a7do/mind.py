from typing import Dict, Any, List
from collections import defaultdict
from a7do.sleep import SleepEngine

class A7DOMind:
    """
    Non-aware learner:
    - event memory
    - lexicon exposure
    - association edges
    - transaction recording
    - coherence gating
    """
    def __init__(self, world_map, profiles, schedule):
        self.world = world_map
        self.profiles = profiles
        self.schedule = schedule

        self.memory: List[Any] = []
        self.lexicon: Dict[str, int] = {}
        self.edges = defaultdict(int)
        self.trace: List[Dict[str, Any]] = []

        self.sleep_engine = SleepEngine()
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
            if place.kind in ("hospital", "house") and ev.room not in place.rooms:
                issues.append(f"unknown_room:{ev.room}")

        # agent can be A7DO or in profiles
        agent_ok = (ev.agent == "A7DO") or (ev.agent in self.profiles.people) or (ev.agent in self.profiles.animals)
        if not agent_ok:
            issues.append(f"unknown_agent:{ev.agent}")

        # object can be None, speech token, or a profile object/animal/person name
        if ev.obj:
            ok = (ev.obj in self.profiles.objects) or (ev.obj in self.profiles.animals) or (ev.obj in self.profiles.people)
            # allow simple speech tokens like "hello", "home", "ball" (tracked by lexicon)
            if not ok and len(ev.obj) > 0:
                # do NOT block; flag as floating token
                issues.append(f"floating_token:{ev.obj}")

        score = 1.0 if not issues else max(0.0, 1.0 - 0.2 * len(issues))
        return {"score": round(score, 2), "issues": issues}

    def ingest(self, ev) -> Dict[str, Any]:
        coh = self.coherence_check(ev)
        self.last_coherence = coh

        if coh["score"] <= 0.2:
            self.last_action = "blocked"
            self.trace.append({"phase": "blocked", "prompt": ev.prompt(), "coherence": coh})
            return {"ok": False, "blocked": True, "coherence": coh}

        # apply movement
        if ev.to_place_id:
            self.schedule.spatial.place_id = ev.to_place_id
        if ev.to_room:
            self.schedule.spatial.room = ev.to_room
        if ev.pos_xyz:
            self.schedule.spatial.pos_xyz = ev.pos_xyz
        if ev.motor.get("type"):
            self.schedule.spatial.locomotion = ev.motor.get("type")

        # store memory
        self.memory.append(ev)

        # lexicon exposure
        self._inc(ev.place_id)
        self._inc(ev.room)
        self._inc(ev.agent)
        self._inc(ev.action)
        if ev.obj:
            self._inc(ev.obj)
        for w in ev.emphasis:
            self._inc(w)
        if ev.sound: self._inc("sound")
        if ev.smell: self._inc("smell")
        if ev.touch: self._inc("touch")
        if ev.motor: self._inc("motor")

        # association edges
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
        if ev.to_place_id:
            tp = f"place:{ev.to_place_id}"
            self.edges[(p, tp)] += 1

        # transaction logging for social
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
                "emphasis": ev.emphasis,
                "sound": ev.sound,
                "smell": ev.smell,
                "touch": ev.touch,
                "motor": ev.motor,
                "to_place_id": ev.to_place_id,
                "to_room": ev.to_room,
                "pos_xyz": ev.pos_xyz,
                "body": ev.body,
                "transaction": ev.transaction,
                "narrator": ev.narrator,
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