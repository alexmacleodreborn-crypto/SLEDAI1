# a7do/newborn_routine.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional
import random
from a7do.events import ExperienceEvent

@dataclass
class TimeCompression:
    real_minutes_per_event: int = 30
    sim_seconds_per_event: int = 30

@dataclass
class NewbornConfig:
    days: int = 20
    learning_events_per_day: int = 15
    feed_interval_hours: int = 2
    change_interval_hours: int = 2
    sleep_blocks: Optional[List[Dict[str, int]]] = None  # e.g. [{"start":0,"hours":2}, ...]
    transport_modes: List[str] = None

    def __post_init__(self):
        if self.transport_modes is None:
            self.transport_modes = ["car", "buggy", "bus"]

class NewbornRoutine:
    """
    Observer-side generator for newborn routines.
    Produces a grounded list of ExperienceEvent entries for a given day.
    """

    def __init__(self, seed: int = 7, config: Optional[NewbornConfig] = None):
        self.seed = seed
        self.cfg = config or NewbornConfig()

    def build_day(self, day: int, overnight_in_hospital: bool = False) -> List[ExperienceEvent]:
        rng = random.Random(self.seed * 10000 + day)
        events: List[ExperienceEvent] = []
        idx = 0

        # Day 0 is special: birth + (overnight OR journey home)
        if day == 0:
            birth = self._birth_block(day, idx)
            events.extend(birth)
            idx = len(events)

            if overnight_in_hospital:
                # Stay in hospital for remainder of Day 0 (a few calm cycles)
                extra = self._hospital_overnight_block(day, idx, rng)
                events.extend(extra)
                idx = len(events)
            else:
                # Journey home on Day 0
                jh = self._journey_home_block(day, idx, rng)
                events.extend(jh)
                idx = len(events)

            # End day in bed at home regardless
            events.extend(self._bed_sleep_block(day, idx))
            return self._reindex(events)

        # Day 1+: standard newborn day anchored at home
        # We generate 15 learning events plus auto feed/change/sleep threads
        schedule = []
        schedule.extend(self._wake_block(day, rng))

        # Create 15 learning events: mix of home scenes and occasional out-of-house
        for _ in range(self.cfg.learning_events_per_day):
            schedule.append(self._learning_event(day, rng))

        # Insert feeding + changing as repeating necessities
        schedule = self._insert_feeds_and_changes(day, schedule, rng)

        # End with sleep
        schedule.extend(self._bed_sleep_block(day, 0))

        return self._reindex(schedule)

    # -------------------------
    # Blocks
    # -------------------------

    def _birth_block(self, day: int, idx: int) -> List[ExperienceEvent]:
        return [
            ExperienceEvent(
                day=day, index=idx, place="hospital",
                people_present=["Mum", "Dad"],
                sensory={"vision": "bright lights", "sound": "voices", "smell": "antiseptic", "touch": "handled"},
                body_effects={"temperature": "cold", "comfort": "low"},
                sounds=["mum", "dad"],
                note="Birth: checks, lights, voices"
            ),
            ExperienceEvent(
                day=day, index=idx+1, place="hospital",
                people_present=["Mum", "Dad", "Nurse"],
                sensory={"sound": "crying", "touch": "wrapped", "vision": "faces close"},
                body_effects={"comfort": "rising"},
                sounds=["nurse", "mum", "dad"],
                note="Birth: wrapped, held, first calm"
            ),
        ]

    def _hospital_overnight_block(self, day: int, idx: int, rng: random.Random) -> List[ExperienceEvent]:
        # gentle repeats: feeding / nappy / sleep / voices
        out = []
        for k in range(4):
            out.append(ExperienceEvent(
                day=day, index=idx+k, place="hospital",
                people_present=["Mum", "Nurse"],
                sensory={"sound": "quiet ward", "touch": "gentle hold"},
                sounds=["shh", "sleep"],
                note="Hospital overnight: calm ward"
            ))
        return out

    def _journey_home_block(self, day: int, idx: int, rng: random.Random) -> List[ExperienceEvent]:
        mode = rng.choice(["car", "buggy"])
        return [
            ExperienceEvent(
                day=day, index=idx, place="street_main",
                people_present=["Mum", "Dad"],
                sensory={"sound": "traffic", "motion": "moving", "vision": "outside blur"},
                movement={"from": "hospital", "to": "street_main"},
                sounds=["going", "home"],
                note=f"Journey home: {mode} strap, motion"
            ),
            ExperienceEvent(
                day=day, index=idx+1, place="park",
                people_present=["Mum", "Dad"],
                sensory={"vision": "open sky", "sound": "birds", "smell": "grass"},
                sounds=["park"],
                note="Passing park (sound token + sensory)"
            ),
            ExperienceEvent(
                day=day, index=idx+2, place="shops",
                people_present=["Mum", "Dad"],
                sensory={"vision": "bright signs", "sound": "chatter"},
                sounds=["shops"],
                note="Passing shops (sound token + sensory)"
            ),
            ExperienceEvent(
                day=day, index=idx+3, place="house_a7do",
                people_present=["Mum", "Dad"],
                sensory={"sound": "door", "smell": "home fabric"},
                movement={"from": "street_main", "to": "house_a7do"},
                sounds=["home"],
                note="Arrive home"
            ),
        ]

    def _wake_block(self, day: int, rng: random.Random) -> List[ExperienceEvent]:
        return [ExperienceEvent(
            day=day, index=0, place="bedroom_a7do",
            people_present=["Mum"],
            sensory={"sound": "morning voices", "light": "soft"},
            sounds=["good", "morning"],
            note="Wake"
        )]

    def _learning_event(self, day: int, rng: random.Random) -> ExperienceEvent:
        # mostly home; sometimes out (park / shops / doctors)
        r = rng.random()
        if r < 0.75:
            return self._home_scene(day, rng)
        else:
            return self._outing_scene(day, rng)

    def _home_scene(self, day: int, rng: random.Random) -> ExperienceEvent:
        # Example learning scenes: kicking legs, grabbing finger, blanket time, nursery rhyme
        scenes = ["blanket_kick", "grab_finger", "nursery_toes", "look_object"]
        s = rng.choice(scenes)

        if s == "blanket_kick":
            return ExperienceEvent(
                day=day, index=0, place="house_a7do",
                people_present=["Mum"],
                sensory={"touch": "blanket", "vision": "ceiling", "sound": "mum voice"},
                sounds=["kicking", "legs"],
                body_effects={"motor": "legs_kicking"},
                note="Living room blanket: kicking legs prompt"
            )

        if s == "grab_finger":
            return ExperienceEvent(
                day=day, index=0, place="house_a7do",
                people_present=["Mum"],
                sensory={"touch": "finger", "sound": "mum laugh"},
                sounds=["got", "my", "finger"],
                body_effects={"motor": "grasp"},
                note="Grab mum finger: reinforcement"
            )

        if s == "nursery_toes":
            return ExperienceEvent(
                day=day, index=0, place="house_a7do",
                people_present=["Mum"],
                sensory={"touch": "toes", "sound": "sing-song"},
                sounds=["this", "little", "piggy", "toe", "toe", "toe"],
                body_effects={"touch_zone": "feet"},
                note="Nursery rhyme: toe repetition"
            )

        # look_object
        return ExperienceEvent(
            day=day, index=0, place="house_a7do",
            people_present=["Mum"],
            sensory={"vision": "object close", "sound": "labelled slowly"},
            sounds=["look"],
            note="Home object glimpse (future: TV/ball/chair)"
        )

    def _outing_scene(self, day: int, rng: random.Random) -> ExperienceEvent:
        place = rng.choice(["park", "shops", "doctors"])
        mode = rng.choice(self.cfg.transport_modes)

        # Transport sub-event + arrival event (we keep it compact for now)
        return ExperienceEvent(
            day=day, index=0, place=place,
            people_present=["Mum"],
            sensory={"motion": f"{mode} moving", **({"sound": "birds"} if place=="park" else {"sound": "indoor hum"})},
            sounds=[place],
            note=f"Outing: {mode} to {place}"
        )

    def _insert_feeds_and_changes(self, day: int, events: List[ExperienceEvent], rng: random.Random) -> List[ExperienceEvent]:
        """
        Insert feeding + nappy changes roughly every 2 hours.
        We don't simulate clock time precisely here; we weave them every ~4 events.
        """
        out = []
        feed_every = 4
        change_every = 4
        for i, ev in enumerate(events):
            out.append(ev)

            if i > 0 and i % feed_every == 0:
                out.append(ExperienceEvent(
                    day=day, index=0, place="house_a7do",
                    people_present=["Mum"],
                    sensory={"touch": "held", "sound": "soft voice"},
                    sounds=["feed"],
                    body_effects={"hunger": "reduced"},
                    note="Feeding routine (~2h)"
                ))
            if i > 0 and i % change_every == 0:
                out.append(ExperienceEvent(
                    day=day, index=0, place="house_a7do",
                    people_present=["Mum"],
                    sensory={"touch": "change", "sound": "rustle"},
                    sounds=["change"],
                    body_effects={"discomfort": "reduced"},
                    note="Nappy change routine (~2h)"
                ))
        return out

    def _bed_sleep_block(self, day: int, idx: int) -> List[ExperienceEvent]:
        return [
            ExperienceEvent(
                day=day, index=idx, place="bedroom_a7do",
                people_present=["Mum"],
                sensory={"sound": "quiet", "light": "dark", "touch": "blanket"},
                sounds=["sleep"],
                body_effects={"sleep": "onset"},
                note="Bedtime sleep"
            )
        ]

    # -------------------------
    # Helpers
    # -------------------------

    def _reindex(self, events: List[ExperienceEvent]) -> List[ExperienceEvent]:
        for i, ev in enumerate(events):
            ev.index = i
        return events