# world_frame/event_generator.py

import random
from typing import List

from world_frame.world_state import WorldEvent, WorldState


class WorldEventGenerator:
    """
    Generates objective world events based on time, place, and routines.
    This is caregiver / environment logic, not intelligence.
    """

    def __init__(self):
        self.last_generated_time: float = -1.0

    def generate(self, world: WorldState) -> List[WorldEvent]:
        """
        Generate new world events if time has advanced.
        """
        events: List[WorldEvent] = []

        # Prevent duplicate generation at same time
        if world.time == self.last_generated_time:
            return events

        self.last_generated_time = world.time

        # -------------------------------------------------
        # Birth & hospital care
        # -------------------------------------------------
        if world.birthed and world.current_place == "Hospital":
            events.append(
                WorldEvent(
                    time=world.time,
                    place="Hospital",
                    description="Nurse checks vital signs",
                    tags=["care", "touch", "voice"],
                )
            )

            if random.random() < 0.3:
                events.append(
                    WorldEvent(
                        time=world.time,
                        place="Hospital",
                        description="Bright hospital lights overhead",
                        tags=["light", "visual"],
                    )
                )

        # -------------------------------------------------
        # Home routines
        # -------------------------------------------------
        if world.current_place == "Home":
            routine = random.choice(
                [
                    "Parent speaks softly nearby",
                    "Being held gently",
                    "Household background noise",
                    "Warm blanket placed",
                ]
            )

            tag_map = {
                "speaks": ["voice", "sound"],
                "held": ["touch", "comfort"],
                "noise": ["sound"],
                "blanket": ["warmth", "touch"],
            }

            tags = []
            for key, t in tag_map.items():
                if key in routine.lower():
                    tags.extend(t)

            events.append(
                WorldEvent(
                    time=world.time,
                    place="Home",
                    description=routine,
                    tags=tags or ["neutral"],
                )
            )

        return events