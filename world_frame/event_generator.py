# world_frame/event_generator.py

import random
from typing import List

from world_frame.world_state import WorldEvent, WorldState


class WorldEventGenerator:
    """
    Generates objective world events gated by experience phase.
    """

    def __init__(self):
        self.last_generated_time: float = -1.0

    def generate(self, world: WorldState, experience) -> List[WorldEvent]:
        events: List[WorldEvent] = []

        # Prevent duplicate generation at the same world time
        if world.time == self.last_generated_time:
            return events

        self.last_generated_time = world.time

        # -------------------------------------------------
        # BIRTH PHASE – intense sensory onset
        # -------------------------------------------------
        if experience.is_phase("birth"):
            events.append(
                WorldEvent(
                    time=world.time,
                    place="Hospital",
                    description="Sudden bright lights and loud sounds",
                    tags=["birth"],
                    sensory={
                        "visual": ["bright light"],
                        "sound": ["loud noise"],
                        "touch": ["cold air"],
                    },
                )
            )
            return events

        # -------------------------------------------------
        # HOSPITAL PHASE – repeated care and settling
        # -------------------------------------------------
        if experience.is_phase("hospital"):
            events.append(
                WorldEvent(
                    time=world.time,
                    place="Hospital",
                    description="Nurse gently checks body",
                    tags=["care"],
                    sensory={
                        "touch": ["hands", "pressure"],
                        "sound": ["soft voice"],
                        "visual": ["faces"],
                    },
                )
            )

            if random.random() < 0.4:
                events.append(
                    WorldEvent(
                        time=world.time,
                        place="Hospital",
                        description="Bright hospital lights overhead",
                        tags=["light"],
                        sensory={
                            "visual": ["bright light"],
                        },
                    )
                )

            return events

        # -------------------------------------------------
        # JOURNEY HOME PHASE – motion and transition
        # -------------------------------------------------
        if experience.is_phase("journey_home"):
            events.append(
                WorldEvent(
                    time=world.time,
                    place="Journey",
                    description="Vehicle movement and engine noise",
                    tags=["movement"],
                    sensory={
                        "motion": ["movement"],
                        "sound": ["engine noise"],
                        "visual": ["passing light"],
                    },
                )
            )
            return events

        # -------------------------------------------------
        # HOME DAY PHASE – stable environment
        # -------------------------------------------------
        if experience.is_phase("home_day"):
            routine = random.choice(
                [
                    WorldEvent(
                        time=world.time,
                        place="Home",
                        description="Parent speaks softly nearby",
                        tags=["care"],
                        sensory={"sound": ["soft voice"]},
                    ),
                    WorldEvent(
                        time=world.time,
                        place="Home",
                        description="Being held gently",
                        tags=["comfort"],
                        sensory={"touch": ["warm arms"]},
                    ),
                    WorldEvent(
                        time=world.time,
                        place="Home",
                        description="Household background noise",
                        tags=["sound"],
                        sensory={"sound": ["muffled noise"]},
                    ),
                    WorldEvent(
                        time=world.time,
                        place="Home",
                        description="Warm blanket placed",
                        tags=["warmth"],
                        sensory={"touch": ["warm fabric"]},
                    ),
                ]
            )
            events.append(routine)
            return events

        return events