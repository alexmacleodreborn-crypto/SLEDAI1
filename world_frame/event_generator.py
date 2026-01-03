# world_frame/event_generator.py

import random
from typing import List

from world_frame.world_state import WorldEvent, WorldState


class WorldEventGenerator:
    """
    Generates objective world events with explicit sensory affordances.
    """

    def __init__(self):
        self.last_generated_time: float = -1.0

    def generate(self, world: WorldState) -> List[WorldEvent]:
        events: List[WorldEvent] = []

        if world.time == self.last_generated_time:
            return events

        self.last_generated_time = world.time

        # ----------------------------
        # Hospital care
        # ----------------------------
        if world.birthed and world.current_place == "Hospital":
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

        # ----------------------------
        # Home routines
        # ----------------------------
        if world.current_place == "Home":
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