# a7do/bot.py
import random

def propose_paths(bot_name, registry, world, profiles, mind):
    """
    Observer-side curriculum bot.
    This function MUST NOT touch A7DO memory directly.
    It only proposes options to the FuturePathRegistry.
    """

    rng = random.Random(world.seed + len(mind.memory) + 777)

    # Read-only signals from A7DO
    lex = mind.lexicon
    cry = mind.schedule.body.cry_level()

    # --- Object grounding proposal ---
    if lex.get("ball", 0) < 3:
        registry.propose(
            type="object",
            proposal={
                "name": "ball",
                "category": "toy",
                "colour": "red",
                "shape": "round",
                "affordances": ["roll", "throw", "catch"],
            },
            unlock={
                "min_day": 0,
                "max_cry": 0.9,
            },
            priority=0.8,
            novelty_cost=0.2,
            notes=[f"{bot_name}: reinforce early object grounding"],
        )

    # --- Movement / park exposure ---
    if cry < 0.8:
        registry.propose(
            type="routine",
            proposal={
                "name": "short_walk_to_park",
                "from": "house_a7do",
                "to": "park_01",
            },
            unlock={
                "min_day": 1,
                "max_cry": 0.8,
            },
            priority=0.6,
            novelty_cost=0.4,
            notes=[f"{bot_name}: introduce outdoor sensory variation"],
        )

    # --- Social expansion (neighbour) ---
    doors = list(getattr(profiles, "neighbour_families", {}).keys())
    if doors:
        door = rng.choice(doors)
        fam = profiles.neighbour_families.get(door, {})
        speaker = fam.get("mum") or fam.get("dad") or fam.get("stepdad")
        if speaker:
            registry.propose(
                type="person",
                proposal={
                    "name": speaker,
                    "door": door,
                    "context": "neighbour_meeting",
                },
                unlock={"min_day": 1},
                priority=0.5,
                novelty_cost=0.3,
                notes=[f"{bot_name}: expand social continuity"],
            )