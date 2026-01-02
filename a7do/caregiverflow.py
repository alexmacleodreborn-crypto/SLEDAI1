# a7do/caregiver_flow.py
from __future__ import annotations

from typing import List
from a7do.events import ExperienceEvent
from a7do.world import WorldState, tick_bot_routines


class CaregiverFlow:
    """
    Observer-side life driver.
    Builds daily experience flows for A7DO without touching cognition.
    """

    def __init__(self, world: WorldState):
        self.world = world

    # =========================
    # PUBLIC API
    # =========================

    def build_day(self, day_index: int, n_events: int = 10) -> List[ExperienceEvent]:
        """
        Build the ordered list of ExperienceEvent objects for a given day.
        """
        if day_index == 0:
            return self._build_birth_day()

        # Advance background bot routines (observer-only)
        tick_bot_routines(self.world, day_index)

        events: List[ExperienceEvent] = []
        idx = 0

        # Morning wake (always at home after day 0)
        events.append(self._wake_event(day_index, idx))
        idx += 1

        # Day activities (caregiver-driven)
        activities = self._day_activities(day_index, n_events - 3)

        for act in activities:
            act.index = idx
            events.append(act)
            idx += 1

        # Return home
        events.append(self._return_home_event(day_index, idx))
        idx += 1

        # Bedtime & sleep
        events.append(self._sleep_event(day_index, idx))

        return events

    # =========================
    # DAY 0 — BIRTH
    # =========================

    def _build_birth_day(self) -> List[ExperienceEvent]:
        """
        One-time origin event.
        Hospital birth → journey home → first sleep.
        """
        return [
            ExperienceEvent(
                day=0,
                index=0,
                place="hospital",
                people_present=["Mum", "Dad"],
                sensory={
                    "vision": "bright lights",
                    "sound": "voices",
                    "smell": "antiseptic",
                    "touch": "handled",
                },
                body_effects={
                    "temperature": "cold",
                    "comfort": "low",
                },
                note="Birth",
            ),
            ExperienceEvent(
                day=0,
                index=1,
                place="hospital",
                people_present=["Mum", "Dad"],
                sensory={
                    "sound": "crying",
                    "touch": "wrapped",
                },
                body_effects={
                    "comfort": "rising",
                },
                note="Post-birth care",
            ),
            ExperienceEvent(
                day=0,
                index=2,
                place="house_a7do",
                movement={"from": "hospital", "to": "house_a7do"},
                people_present=["Mum", "Dad"],
                sensory={
                    "sound": "car noise",
                    "motion": "rocking",
                },
                note="Journey home",
            ),
            ExperienceEvent(
                day=0,
                index=3,
                place="bedroom_a7do",
                people_present=["Mum"],
                sensory={
                    "sound": "quiet",
                    "smell": "bedding",
                },
                body_effects={
                    "comfort": "high",
                    "sleep": "onset",
                },
                note="First sleep",
            ),
        ]

    # =========================
    # DAILY BUILDING BLOCKS
    # =========================

    def _wake_event(self, day: int, idx: int) -> ExperienceEvent:
        return ExperienceEvent(
            day=day,
            index=idx,
            place="bedroom_a7do",
            people_present=["Mum"],
            sensory={
                "sound": "morning voices",
                "light": "soft",
            },
            body_effects={
                "sleep": "ended",
            },
            note="Wake",
        )

    def _day_activities(self, day: int, count: int) -> List[ExperienceEvent]:
        """
        Build caregiver-led daytime activities.
        """
        activities: List[ExperienceEvent] = []

        # Simple deterministic rotation for now
        options = ["park", "shops", "home"]

        for i in range(count):
            place = options[(day + i) % len(options)]

            people = ["Mum"]
            pets = []
            sounds = []

            # Social overlap examples
            if place == "park":
                people.append("Lucy")
                pets.append("Millie")
                sounds.extend(["Lucy", "Millie"])

            activities.append(
                ExperienceEvent(
                    day=day,
                    index=0,  # filled later
                    place=place,
                    people_present=people,
                    pets_present=pets,
                    sensory=self.world.get_sensory(place),
                    sounds=sounds,
                    note=f"Day activity at {place}",
                )
            )

        return activities

    def _return_home_event(self, day: int, idx: int) -> ExperienceEvent:
        return ExperienceEvent(
            day=day,
            index=idx,
            place="house_a7do",
            movement={"from": "outside", "to": "house_a7do"},
            people_present=["Mum"],
            sensory={
                "sound": "door closing",
            },
            note="Return home",
        )

    def _sleep_event(self, day: int, idx: int) -> ExperienceEvent:
        return ExperienceEvent(
            day=day,
            index=idx,
            place="bedroom_a7do",
            people_present=["Mum"],
            sensory={
                "sound": "quiet",
                "light": "dark",
            },
            body_effects={
                "sleep": "onset",
            },
            note="Sleep",
        )