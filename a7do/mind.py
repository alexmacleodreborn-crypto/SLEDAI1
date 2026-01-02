# a7do/mind.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
from a7do.body import BiologicalState
from a7do.somatic import SomaticState
from a7do.events import ExperienceEvent


class A7DOMind:
    """
    Minimal mind loop for this phase:
    - records traces (observations)
    - tracks a simple lexicon exposure counter
    - logs internal activity timeline
    """

    def __init__(self):
        self.body = BiologicalState()
        self.somatic = SomaticState()

        self.day = 0
        self.trace: List[Dict[str, Any]] = []
        self.activity: List[Dict[str, Any]] = []   # "thinking timeline"
        self.lexicon: Dict[str, int] = {}
        self.last_action: str = "waiting"

    def _log(self, kind: str, **payload):
        self.activity.append({"kind": kind, **payload})

    def ingest(self, ev: ExperienceEvent, day: int, event_index: int):
        # Internal processing markers
        self.last_action = f"ingest event {event_index}"
        self._log("ingest", day=day, event=event_index, place=ev.place_id, room=ev.room)

        # Body drift while awake
        self.body.update()
        self.somatic.decay()

        # Lexicon exposure: spoken tokens + emphasis
        for tok in (ev.sounds_spoken or []):
            t = str(tok).strip().lower()
            if t:
                self.lexicon[t] = self.lexicon.get(t, 0) + 1

        for tok in (ev.emphasis or []):
            t = str(tok).strip().lower()
            if t:
                self.lexicon[t] = self.lexicon.get(t, 0) + 2  # emphasis weighs more

        # Observational trace: co-presence in a place
        if ev.presence:
            for person in ev.presence:
                if person and person not in ("Mum", "Dad", "Sister"):
                    self.trace.append({
                        "day": day,
                        "event": event_index,
                        "place": ev.place_id,
                        "saw": person,
                        "with": [p for p in ev.presence if p and p != person],
                        "pets": list(ev.pets or []),
                        "action": ev.action,
                        "object": ev.obj,
                    })
                    self._log("trace_write", day=day, event=event_index, saw=person, place=ev.place_id)

        # Somatic hooks (optional, safe defaults)
        if ev.touch.get("pattern"):
            self.somatic.apply_touch("chest", 0.15)

        # Store body snapshot into event for observer visibility
        ev.body = self.body.snapshot()
        self._log("body", day=day, event=event_index, **ev.body)

    def sleep(self, day: int):
        self.last_action = "sleep"
        self._log("sleep_start", day=day)
        self.body.sleep()
        # In this phase, “sleep” does not invent meaning; it just marks consolidation.
        self._log("sleep_end", day=day, body=self.body.snapshot())

    def known_words(self) -> Dict[str, int]:
        return dict(sorted(self.lexicon.items(), key=lambda x: (-x[1], x[0])))

    def summary(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "last_action": self.last_action,
            "body": self.body.snapshot(),
            "somatic": self.somatic.snapshot(),
            "lexicon_size": len(self.lexicon),
            "trace_count": len(self.trace),
            "activity_len": len(self.activity),
        }