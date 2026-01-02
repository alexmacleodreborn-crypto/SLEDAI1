# a7do/homeplot.py

from dataclasses import dataclass
from typing import Dict, Tuple
import random


@dataclass
class Room:
    name: str
    size: Tuple[int, int]   # width, depth
    colour: str
    features: Dict[str, str]


@dataclass
class Place:
    place_id: str
    label: str
    pos_xyz: Tuple[int, int, int]
    rooms: Dict[str, Room]


def generate_default_home(seed: int = 42) -> Place:
    """
    Generate a stable, observer-defined home.
    This is NOT A7DO knowledge — this is world truth.
    """

    rng = random.Random(seed)

    wall_colours = ["cream", "light blue", "soft green", "warm white"]
    bedroom_features = {
        "bed": "soft",
        "window": "curtains",
        "floor": "carpet",
    }

    rooms = {
        "living_room": Room(
            name="Living Room",
            size=(5, 4),
            colour=rng.choice(wall_colours),
            features={
                "sofa": "fabric",
                "table": "wood",
                "window": "large",
            },
        ),
        "kitchen": Room(
            name="Kitchen",
            size=(4, 3),
            colour=rng.choice(wall_colours),
            features={
                "sink": "metal",
                "cupboard": "wood",
                "floor": "tile",
            },
        ),
        "bathroom": Room(
            name="Bathroom",
            size=(3, 2),
            colour="white",
            features={
                "bath": "ceramic",
                "toilet": "ceramic",
                "floor": "tile",
            },
        ),
        "bedroom_a7do": Room(
            name="A7DO Bedroom",
            size=(3, 3),
            colour=rng.choice(wall_colours),
            features=bedroom_features,
        ),
    }

    return Place(
        place_id="house_a7do",
        label="Home",
        pos_xyz=(0, 0, 0),
        rooms=rooms,
    )