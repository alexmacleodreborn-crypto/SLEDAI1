# a7do/daybuilder.py

import random
from a7do.events import ExperienceEvent


def build_day_events(
    day: int,
    world,
    profiles,
    schedule,
    mind,
    n_events: int = 10,
):
    rng = random.Random(world.seed + day)

    events = []
    place_id = "house_a7do"
    room = "living_room"

    parents = list(profiles.people.keys())
    cry = schedule.body.cry_level()

    for i in range(n_events):
        # If distressed, only soothing events
        if cry > 0.7:
            events.append(
                ExperienceEvent(
                    place_id=place_id,
                    room=room,
                    agent="Mum",
                    action="held",
                    obj="you",
                    sound={"pattern": "soft voice"},
                    touch={"pattern": "warm arms"},
                    presence=["Mum"],
                    body=schedule.body.snapshot(),
                )
            )
            cry *= 0.85
            continue

        action_type = rng.choice(
            ["show_object", "name_person", "ambient", "movement"]
        )

        # ─── Object exposure
        if action_type == "show_object" and profiles.objects:
            obj = rng.choice(list(profiles.objects.keys()))
            events.append(
                ExperienceEvent(
                    place_id=place_id,
                    room=room,
                    agent="Dad",
                    action="showed",
                    obj=obj,
                    emphasis=[obj.upper()],
                    sound={"pattern": "clear voice"},
                    presence=["Dad", "Mum"],
                    body=schedule.body.snapshot(),
                )
            )

        # ─── Person naming
        elif action_type == "name_person":
            p = rng.choice(parents)
            events.append(
                ExperienceEvent(
                    place_id=place_id,
                    room=room,
                    agent="Dad",
                    action="said",
                    obj=p,
                    emphasis=[p.upper()],
                    sound={"pattern": "introducing voice"},
                    presence=["Dad", "Mum"],
                    body=schedule.body.snapshot(),
                )
            )

        # ─── Ambient sensory
        elif action_type == "ambient":
            events.append(
                ExperienceEvent(
                    place_id=place_id,
                    room=room,
                    agent="Environment",
                    action="felt",
                    sound={"pattern": rng.choice(["quiet", "house noise"])},
                    smell={"pattern": rng.choice(["clean", "food"])},
                    presence=["Mum", "Dad"],
                    body=schedule.body.snapshot(),
                )
            )

        # ─── Movement
        else:
            events.append(
                ExperienceEvent(
                    place_id=place_id,
                    room=room,
                    agent="Mum",
                    action="carried",
                    obj="you",
                    motor={"type": "carry"},
                    presence=["Mum"],
                    body=schedule.body.snapshot(),
                )
            )

    return events