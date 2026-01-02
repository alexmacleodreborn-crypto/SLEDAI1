#a7do/boy.py

import random

def propose_paths(bot_name: str, registry, world, profiles, mind):
    rng = random.Random(world.seed + len(mind.memory) + 777)

    ball_seen = mind.lexicon.get("ball", 0)
    cry = mind.schedule.body.cry_level()

    if ball_seen < 3:
        registry.propose(
            type="object",
            proposal={"name": "ball", "category": "toy", "colour": "red", "shape": "round", "affordances": ["roll", "catch"]},
            unlock={"min_lexicon": {"ball": 1}, "max_cry": 0.9},
            priority=0.8,
            novelty_cost=0.2,
            notes=[f"{bot_name}: reinforce early toy grounding"]
        )

    if cry < 0.8:
        registry.propose(
            type="routine",
            proposal={"name": "short_walk_to_park", "from": "house_a7do", "to": "park_01"},
            unlock={"min_day": 1, "max_cry": 0.8},
            priority=0.6,
            novelty_cost=0.4,
            notes=[f"{bot_name}: introduce park sensory"]
        )

    doors = list(profiles.neighbour_families.keys())
    if doors:
        d = rng.choice(doors)
        fam = profiles.neighbour_families.get(d, {})
        speaker = fam.get("mum") or fam.get("dad") or fam.get("stepdad")
        if speaker:
            registry.propose(
                type="person",
                proposal={"name": speaker, "door": d, "context": "neighbour_meeting"},
                unlock={"min_day": 1},
                priority=0.5,
                novelty_cost=0.3,
                notes=[f"{bot_name}: expand social continuity"]
            )