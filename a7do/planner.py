import random
from typing import Dict, List
from a7do.events import ExperienceEvent

def _rand_pos(rng):
    return (round(rng.uniform(0.2, 0.8), 2), round(rng.uniform(0.2, 0.8), 2))

def make_parent_knowledge(seed: int) -> List[str]:
    rng = random.Random(seed)
    facts = [
        "tools go in the toolbox",
        "food is in the kitchen",
        "bathroom is for washing",
        "park has swings",
        "dogs can bark",
        "balls can roll",
        "bed is for sleeping",
        "street connects houses",
        "windows let in light",
        "rain makes things wet",
    ]
    rng.shuffle(facts)
    return facts[:4]

def generate_day(world_map, profiles, schedule, day: int, seed: int = 11) -> List[ExperienceEvent]:
    rng = random.Random(seed + day)

    # parents
    mum = next((p.name for p in profiles.people.values() if p.role.lower() == "mum"), None)
    dad = next((p.name for p in profiles.people.values() if p.role.lower() == "dad"), None)
    if not mum or not dad:
        return []

    # default objects / animals if exist
    ball = "ball" if "ball" in profiles.objects else None
    dog = next(iter(profiles.animals.keys()), None)

    # Body tick → may cause a cry event
    schedule.body.tick_awake()
    cry = schedule.body.cry_level()

    evs: List[ExperienceEvent] = []

    # Wake event always
    evs.append(ExperienceEvent(
        building="House_A7DO", room="bedroom_child",
        agent=mum, action="said", obj="hello",
        emphasis=["hello"],
        sound={"source": mum, "pattern": "soft voice", "volume": "soft"},
        motor={"type": "still", "intensity": "low"},
        pos_xy=_rand_pos(rng),
        body=schedule.body.snapshot()
    ))

    # Biological crying event if high
    if cry > 0.75:
        evs.append(ExperienceEvent(
            building="House_A7DO", room="bedroom_child",
            agent="A7DO", action="cried", obj=None,
            emphasis=["cry"],
            sound={"source": "A7DO", "pattern": "cry", "volume": "loud"},
            motor={"type": "wiggle", "intensity": "high"},
            pos_xy=_rand_pos(rng),
            body=schedule.body.snapshot()
        ))
        # Dad responds: feed
        schedule.body.feed()
        evs.append(ExperienceEvent(
            building="House_A7DO", room="bedroom_child",
            agent=dad, action="fed", obj="milk",
            emphasis=["milk"],
            sound={"source": dad, "pattern": "shush", "volume": "soft"},
            pos_xy=_rand_pos(rng),
            body=schedule.body.snapshot()
        ))

    # Movement: bedroom -> hall
    evs.append(ExperienceEvent(
        building="House_A7DO", room="bedroom_child",
        agent=dad, action="carried", obj="you",
        emphasis=["hall"],
        motor={"type": "carried", "intensity": "steady"},
        to_room="hall",
        pos_xy=_rand_pos(rng),
        body=schedule.body.snapshot()
    ))

    # Ball learning event: situated + emphasis
    if ball:
        evs.append(ExperienceEvent(
            building="House_A7DO", room="living_room",
            agent=dad, action="rolled", obj=ball,
            emphasis=["ball", "BALL"],
            sound={"source": dad, "pattern": "clap", "volume": "soft"},
            motor={"type": "crawl", "intensity": "slow"},
            pos_xy=_rand_pos(rng),
            body=schedule.body.snapshot()
        ))
        evs.append(ExperienceEvent(
            building="House_A7DO", room="living_room",
            agent=dad, action="said", obj="catch",
            emphasis=["catch", "ball"],
            pos_xy=_rand_pos(rng),
            body=schedule.body.snapshot()
        ))

    # Dog intro on Day 1
    if day >= 1 and dog:
        evs.append(ExperienceEvent(
            building="House_A7DO", room="kitchen",
            agent=mum, action="showed", obj=dog,
            emphasis=[dog],
            sound={"source": dog, "pattern": "bark", "volume": "low"},
            pos_xy=_rand_pos(rng),
            body=schedule.body.snapshot()
        ))

    # Cap infant dose
    return evs[:8]