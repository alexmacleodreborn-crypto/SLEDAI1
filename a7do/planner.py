import random
from typing import List
from a7do.events import ExperienceEvent

def _pos(rng, base):
    bx, by, bz = base
    return (round(bx + rng.uniform(-0.5, 0.5), 2), round(by + rng.uniform(-0.5, 0.5), 2), round(bz + rng.uniform(0.0, 0.5), 2))

def birth_sequence(world, schedule, mum="Mum", dad="Dad") -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 100)
    schedule.body.tick_awake()
    base = world.places["hospital_cwh"].pos_xyz

    evs = []
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent="Nurse", action="checked", obj="health",
        narrator="Health checks under bright lights",
        sound={"pattern": "voices echo", "volume": "medium"},
        smell={"pattern": "clean chemical"},
        touch={"pattern": "gentle hands", "temp": "cool"},
        motor={"type": "newborn", "intensity": "low"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=["Nurse"]
    ))

    cry = schedule.body.cry_level()
    if cry > 0.65:
        evs.append(ExperienceEvent(
            place_id="hospital_cwh", room="delivery_room",
            agent="A7DO", action="cried",
            narrator="Newborn cry response",
            sound={"pattern": "cry", "volume": "loud"},
            motor={"type": "wiggle", "intensity": "high"},
            pos_xyz=_pos(rng, base),
            body=schedule.body.snapshot(),
            transaction={"target": "A7DO", "outcome": "cried"}
        ))

    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=mum, action="held", obj="you",
        narrator="Mum voice + smell imprint",
        sound={"pattern": "soft voice"},
        smell={"pattern": "warm skin"},
        touch={"pattern": "soft cloth", "temp": "warm"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[mum, "Nurse"]
    ))

    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=dad, action="spoke", obj="hello",
        narrator="Dad voice imprint",
        sound={"pattern": "deep voice", "volume": "medium"},
        smell={"pattern": "outdoor air"},
        touch={"pattern": "firm hold", "temp": "warm"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[dad, mum]
    ))

    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=mum, action="said", obj="Hospital Street",
        narrator="Street name as sound token",
        sound={"pattern": "soft voice"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[mum, dad]
    ))

    return evs

def drive_home_sequence(world, schedule, mum="Mum", dad="Dad") -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 200)
    schedule.body.tick_awake()

    park = world.places["park_01"].pos_xyz
    shops = world.places["shops_01"].pos_xyz
    home_st = world.places["street_home"].pos_xyz

    evs = []
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=dad, action="carried", obj="you",
        narrator="Leaving hospital",
        motor={"type": "carried", "intensity": "steady"},
        to_place_id="park_01",
        pos_xyz=_pos(rng, park),
        sound={"pattern": "doors"},
        body=schedule.body.snapshot(),
        presence=[dad, mum]
    ))

    evs.append(ExperienceEvent(
        place_id="park_01", room="",
        agent=mum, action="said", obj="Park Lane",
        narrator="Passing park",
        sound={"pattern": "car hum"},
        motor={"type": "car", "intensity": "steady"},
        to_place_id="shops_01",
        pos_xyz=_pos(rng, shops),
        body=schedule.body.snapshot(),
        presence=[mum, dad]
    ))

    evs.append(ExperienceEvent(
        place_id="shops_01", room="",
        agent=dad, action="said", obj="Market Road",
        narrator="Passing shops",
        sound={"pattern": "traffic"},
        smell={"pattern": "food"},
        motor={"type": "car", "intensity": "steady"},
        to_place_id="street_home",
        pos_xyz=_pos(rng, home_st),
        body=schedule.body.snapshot(),
        presence=[dad, mum]
    ))

    evs.append(ExperienceEvent(
        place_id="street_home", room="",
        agent=mum, action="said", obj="Home Street",
        narrator="Arriving home street",
        sound={"pattern": "car slow"},
        motor={"type": "car", "intensity": "low"},
        body=schedule.body.snapshot(),
        presence=[mum, dad]
    ))

    return evs

def arrive_home_sequence(world, schedule, mum="Mum", dad="Dad", sister_name="Sister") -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 300)
    schedule.body.tick_awake()

    base = world.places["house_a7do"].pos_xyz
    evs = []

    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent=dad, action="said", obj="this is our home",
        narrator="Home anchored",
        emphasis=["home"],
        sound={"pattern": "calm voice"},
        smell={"pattern": "house neutral"},
        motor={"type": "carried", "intensity": "low"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[dad, mum]
    ))

    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent=mum, action="said", obj="blue door",
        narrator="Door colour described",
        emphasis=["blue"],
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[mum, dad]
    ))

    evs.append(ExperienceEvent(
        place_id="house_a7do", room="living_room",
        agent=sister_name, action="spoke", obj="hi",
        narrator="Sister voice pattern begins",
        sound={"pattern": "small voice"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[sister_name, mum, dad],
        transaction={"target": "A7DO", "outcome": "calm"}
    ))

    evs.append(ExperienceEvent(
        place_id="house_a7do", room="living_room",
        agent=dad, action="said", obj="Xena",
        narrator="Pet name seeded as token",
        sound={"pattern": "excited voice"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        presence=[dad, mum, sister_name]
    ))

    return evs