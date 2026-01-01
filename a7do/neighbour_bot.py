# a7do/neighbour_bot.py
import random

def propose_neighbour_visit(registry, world, profiles, mind):
    """
    Propose a single neighbour visit as a future path.
    """
    # Preconditions
    if mind.schedule.spatial.place_id != "house_a7do":
        return

    cry = mind.schedule.body.cry_level()
    if cry > 0.7:
        return  # too distressed

    doors = list(profiles.neighbour_families.keys())
    if not doors:
        return

    rng = random.Random(world.seed + len(mind.memory))
    door = rng.choice(doors)
    fam = profiles.neighbour_families.get(door, {})

    visitor = fam.get("mum") or fam.get("dad") or fam.get("stepdad")
    if not visitor:
        return

    registry.propose(
        type="routine",
        proposal={
            "name": "neighbour_visit",
            "door": door,
            "visitor": visitor,
            "place": "house_a7do",
        },
        unlock={
            "min_day": 0,
            "place": "house_a7do",
            "max_cry": 0.7,
        },
        priority=0.7,
        novelty_cost=0.3,
        notes=[f"Neighbour {visitor} from door {door} visits briefly"],
    )