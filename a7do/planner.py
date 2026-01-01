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

    # Sensory imprint cluster
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent="Nurse", action="checked", obj="health",
        narrator="Health checks under bright lights",
        sound={"pattern": "voices echo", "volume": "medium"},
        smell={"pattern": "clean chemical"},
        touch={"pattern": "gentle hands", "temp": "cool"},
        motor={"type": "newborn", "intensity": "low"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # Cry signal
    cry = schedule.body.cry_level()
    if cry > 0.65:
        evs.append(ExperienceEvent(
            place_id="hospital_cwh", room="delivery_room",
            agent="A7DO", action="cried", obj=None,
            narrator="Newborn cry in response to discomfort",
            sound={"pattern": "cry", "volume": "loud"},
            touch={"pattern": "air cool"},
            motor={"type": "wiggle", "intensity": "high"},
            pos_xyz=_pos(rng, base),
            body=schedule.body.snapshot(),
            transaction={"target": "A7DO", "outcome": "cried"}
        ))

    # Mum contact (pattern)
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=mum, action="held", obj="you",
        narrator="Mum voice + smell imprint",
        sound={"pattern": "soft voice", "volume": "soft"},
        smell={"pattern": "warm skin"},
        touch={"pattern": "soft cloth", "temp": "warm"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # Dad contact (different pattern)
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=dad, action="spoke", obj="hello",
        narrator="Dad voice + irregular cough/sneeze nearby",
        sound={"pattern": "deep voice + cough", "volume": "medium"},
        smell={"pattern": "outdoor air"},
        touch={"pattern": "firm hold", "temp": "warm"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # Context seeding (street names as floating tokens)
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=mum, action="said", obj="Hospital Street",
        narrator="Parent mentions hospital street",
        sound={"pattern": "soft voice"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    return evs

def drive_home_sequence(world, schedule, mum="Mum", dad="Dad") -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 200)
    schedule.body.tick_awake()

    base = world.places["hospital_cwh"].pos_xyz
    park = world.places["park_01"].pos_xyz
    shops = world.places["shops_01"].pos_xyz
    home_st = world.places["street_home"].pos_xyz

    evs = []

    # leaving hospital (movement)
    evs.append(ExperienceEvent(
        place_id="hospital_cwh", room="delivery_room",
        agent=dad, action="carried", obj="you",
        narrator="Leaving hospital; movement begins",
        motor={"type": "carried", "intensity": "steady"},
        to_place_id="park_01",
        to_room="",
        pos_xyz=_pos(rng, park),
        sound={"pattern": "doors", "volume": "medium"},
        body=schedule.body.snapshot()
    ))

    # pass park (speech + motion)
    evs.append(ExperienceEvent(
        place_id="park_01", room="",
        agent=mum, action="said", obj="Park Lane",
        narrator="Passing park; parent mentions park street",
        sound={"pattern": "car hum", "volume": "low"},
        motor={"type": "car", "intensity": "steady"},
        to_place_id="shops_01",
        pos_xyz=_pos(rng, shops),
        body=schedule.body.snapshot()
    ))

    # pass shops
    evs.append(ExperienceEvent(
        place_id="shops_01", room="",
        agent=dad, action="said", obj="Market Road",
        narrator="Passing shops; parent mentions shops street",
        sound={"pattern": "traffic", "volume": "medium"},
        smell={"pattern": "food"},
        motor={"type": "car", "intensity": "steady"},
        to_place_id="street_home",
        pos_xyz=_pos(rng, home_st),
        body=schedule.body.snapshot()
    ))

    # approach home street
    evs.append(ExperienceEvent(
        place_id="street_home", room="",
        agent=mum, action="said", obj="Home Street",
        narrator="Arriving near home street",
        sound={"pattern": "car slow", "volume": "low"},
        motor={"type": "car", "intensity": "low"},
        body=schedule.body.snapshot()
    ))

    return evs

def arrive_home_sequence(world, schedule, mum="Mum", dad="Dad", sister_name="Sister") -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 300)
    schedule.body.tick_awake()

    home = world.places["house_a7do"]
    base = home.pos_xyz

    evs = []

    # home declaration (anchoring)
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent=dad, action="said", obj="this is our home",
        narrator="Home anchored + described",
        emphasis=["home"],
        sound={"pattern": "calm voice", "volume": "soft"},
        smell={"pattern": "house neutral"},
        motor={"type": "carried", "intensity": "low"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # door colour + levels + gardens
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent=mum, action="said", obj="blue door",
        narrator="Door colour described",
        emphasis=["blue"],
        sound={"pattern": "soft voice"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent=mum, action="said", obj="two levels",
        narrator="Levels described",
        emphasis=["upstairs"],
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # sister introduction
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="living_room",
        agent=sister_name, action="spoke", obj="hi",
        narrator="Sister appears; voice pattern begins",
        sound={"pattern": "small voice", "volume": "soft"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot(),
        transaction={"target": "A7DO", "outcome": "calm"}
    ))

    # pet mention -> pet appears later; keep as floating token here
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="living_room",
        agent=dad, action="said", obj="Xena",
        narrator="Pet name exposed before full grounding",
        sound={"pattern": "excited voice", "volume": "medium"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    return evs

def neighbourhood_meeting_sequence(world, profiles, schedule, doors: List[str]) -> List[ExperienceEvent]:
    rng = random.Random(world.seed + 400 + schedule.day)
    schedule.body.tick_awake()

    evs = []
    base = world.places["house_a7do"].pos_xyz

    # Ambient street noise first (no entities)
    evs.append(ExperienceEvent(
        place_id="house_a7do", room="hall",
        agent="Street", action="sounded", obj="neighbours",
        narrator="Background doors, distant voices, dogs, cars",
        sound={"pattern": "distant voices + doors", "volume": "low"},
        pos_xyz=_pos(rng, base),
        body=schedule.body.snapshot()
    ))

    # Introductions: a subset per meeting to avoid overload
    sample_doors = rng.sample(doors, k=min(6, len(doors)))

    for door in sample_doors:
        fam = profiles.neighbour_families.get(door, {})
        # choose one representative adult to introduce
        speaker = fam.get("mum") or fam.get("dad") or fam.get("stepdad") or "Neighbour"
        if speaker not in profiles.people:
            continue

        # A7DO reaction: if body cry is high, more likely cry
        cry = schedule.body.cry_level()
        outcome = "cried" if cry > 0.75 and rng.random() < 0.7 else "calm"

        # greeting event
        evs.append(ExperienceEvent(
            place_id="house_a7do", room="living_room",
            agent=speaker, action="said", obj=f"my name is {speaker}",
            narrator=f"Neighbour from door {door} introduces self; door colour {world.places.get('house_n_'+door).meta.get('door_colour','') if ('house_n_'+door) in world.places else ''}",
            sound={"pattern": "hello voice", "volume": "medium"},
            smell={"pattern": "perfume" if rng.random() < 0.5 else "outdoor"},
            touch={"pattern": "cuddle" if rng.random() < 0.5 else "pat"},
            pos_xyz=_pos(rng, base),
            body=schedule.body.snapshot(),
            transaction={"target": "A7DO", "outcome": outcome}
        ))

        # if cried, parent soothes
        if outcome == "cried":
            schedule.body.feed()  # calming proxy
            evs.append(ExperienceEvent(
                place_id="house_a7do", room="living_room",
                agent="Mum", action="soothed", obj="shh",
                narrator="Parent soothes after cry",
                sound={"pattern": "shush", "volume": "soft"},
                touch={"pattern": "rocking", "temp": "warm"},
                pos_xyz=_pos(rng, base),
                body=schedule.body.snapshot()
            ))

    return evs