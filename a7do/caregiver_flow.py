# a7do/caregiver_flow.py
from __future__ import annotations
from typing import List
from a7do.events import ExperienceEvent
from a7do.world import WorldState, tick_bot_routines


class CaregiverFlow:
    """
    Builds grounded daily event sequences driven by Mum/Dad routines.
    Names are treated as sound tokens, not knowledge.
    """

    def __init__(self, world: WorldState):
        self.world = world

    def build_day(self, day: int, n_events: int = 10) -> List[ExperienceEvent]:
        # Background bot movement for Observer
        tick_bot_routines(self.world, day)

        events: List[ExperienceEvent] = []

        # Always start at home (except day 0 special-cased by caller if you want)
        # Morning wake / prep
        events.append(ExperienceEvent(
            place_id="house_a7do",
            room="living_room",
            agent="Mum",
            action="prepared",
            obj="you",
            presence=["Mum", "Dad"],
            sound={"pattern": "morning home"},
            touch={"pattern": "warm hands"},
            sounds_spoken=["good morning", "home"],
        ))

        # Decide today's main outing
        # Odd days: park with Lucy & Millie; Even: shops; Day 2: doctors (example)
        if day == 2:
            outing = "doctors"
            outing_label = ["doctor"]
        elif day % 2 == 1:
            outing = "park"
            outing_label = ["park", "Lucy", "Millie"]
        else:
            outing = "groceries"
            outing_label = ["shops", "food"]

        # Transition: home -> street -> outing
        events.append(ExperienceEvent(
            place_id="street_main",
            room="outdoors",
            agent="Dad",
            action="carried",
            obj="you",
            presence=["Dad", "Mum"],
            motor={"type": "carried"},
            sound={"pattern": "street traffic"},
            movement={"from": "house_a7do", "to": "street_main"},
            sounds_spoken=["going out"],
        ))

        events.append(ExperienceEvent(
            place_id=outing,
            room="main",
            agent="Mum",
            action="arrived",
            obj=outing,
            presence=["Mum", "Dad"],
            sound={"pattern": self.world.get_sensory(outing).get("sound", "ambient")},
            smell={"pattern": self.world.get_sensory(outing).get("smell", "mixed")},
            vision={"pattern": self.world.get_sensory(outing).get("vision", "bright")},
            movement={"from": "street_main", "to": outing},
            sounds_spoken=outing_label,
        ))

        # Social overlap at park (if park day)
        if outing == "park":
            events.append(ExperienceEvent(
                place_id="park",
                room="path",
                agent="Mum",
                action="met",
                obj="Lucy",
                presence=["Mum", "Dad", "Lucy"],
                pets=["Millie"],
                sound={"pattern": "birds + voices"},
                smells={"pattern": "grass"} if False else {},  # keep stable; optional
                sounds_spoken=["Lucy", "Millie"],
                emphasis=["LUCY", "MILLIE"],
            ))

            # Optional visit to house 7 later (build place linking)
            events.append(ExperienceEvent(
                place_id="house_7",
                room="front",
                agent="Mum",
                action="visited",
                obj="House 7",
                presence=["Mum", "Lucy"],
                pets=["Millie"],
                sound={"pattern": "door + greeting"},
                movement={"from": "park", "to": "house_7"},
                sounds_spoken=["house seven", "Lucy"],
                emphasis=["HOUSE", "SEVEN"],
            ))

        # Fill remaining events with low-load home routines
        while len(events) < max(1, n_events - 2):
            events.append(ExperienceEvent(
                place_id="house_a7do",
                room="living_room",
                agent="Environment",
                action="settled",
                presence=["Mum"],
                sound={"pattern": "home quiet"},
                smell={"pattern": "fabric"},
                sounds_spoken=["home"],
            ))

        # Return home transition
        events.append(ExperienceEvent(
            place_id="house_a7do",
            room="hall",
            agent="Dad",
            action="returned",
            obj="home",
            presence=["Mum", "Dad"],
            movement={"from": outing, "to": "house_a7do"},
            sounds_spoken=["home"],
        ))

        # Bedtime (MANDATORY)
        events.append(ExperienceEvent(
            place_id="bedroom_a7do",
            room="bed",
            agent="Mum",
            action="put",
            obj="you to bed",
            presence=["Mum"],
            sound={"pattern": "soft voice"},
            touch={"pattern": "blanket"},
            movement={"from": "house_a7do", "to": "bedroom_a7do"},
            sounds_spoken=["sleep", "good night"],
        ))

        return events[:n_events]  # hard cap