from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random

WALL_COLOURS = ["cream", "light blue", "soft green", "white", "light grey", "warm beige"]

@dataclass
class Room:
    name: str
    width_m: float
    length_m: float
    wall_colour: str
    windows: int
    baseline_sound: str
    baseline_smell: str
    fixtures: List[str] = field(default_factory=list)

@dataclass
class Building:
    name: str
    kind: str  # house, park, shop, etc.
    position: Tuple[int, int]  # map coords
    rooms: Dict[str, Room] = field(default_factory=dict)

@dataclass
class WorldMap:
    seed: int
    grid_size: Tuple[int, int] = (8, 6)
    buildings: Dict[str, Building] = field(default_factory=dict)
    streets: List[Tuple[Tuple[int,int], Tuple[int,int]]] = field(default_factory=list)

    def building_names(self):
        return list(self.buildings.keys())

def _rdim(rng, a, b):
    return round(rng.uniform(a, b), 2)

def generate_house_rooms(rng, house_name: str) -> Dict[str, Room]:
    # Basic 2-level concept, but we model rooms only (levels are semantic for later)
    def mk(name, w_rng, l_rng, fixtures, sound, smell):
        return Room(
            name=name,
            width_m=_rdim(rng, *w_rng),
            length_m=_rdim(rng, *l_rng),
            wall_colour=rng.choice(WALL_COLOURS),
            windows=rng.randint(0, 2),
            baseline_sound=sound,
            baseline_smell=smell,
            fixtures=fixtures
        )

    rooms = {
        "hall": mk("hall", (2.0, 3.5), (3.0, 6.0), ["doorway", "coat hook"], "house hum", "neutral"),
        "living_room": mk("living_room", (2.8, 5.5), (3.0, 6.0), ["sofa", "table", "lamp"], "quiet", "neutral"),
        "kitchen": mk("kitchen", (2.5, 5.0), (2.5, 5.5), ["cupboard", "sink", "table"], "clink", "food"),
        "bathroom": mk("bathroom", (1.8, 3.0), (1.8, 3.5), ["toilet", "sink"], "fan", "soap"),
        "bedroom_child": mk("bedroom_child", (2.5, 4.5), (2.5, 5.0), ["bed", "curtains", "toy box"], "quiet", "clean"),
        "bedroom_parent": mk("bedroom_parent", (2.6, 5.0), (2.6, 5.5), ["bed", "wardrobe", "curtains"], "quiet", "clean"),
    }
    return rooms

def generate_neighbourhood(seed: int) -> WorldMap:
    rng = random.Random(seed)
    world = WorldMap(seed=seed)

    # Place the main house
    main_house = Building(
        name="House_A7DO",
        kind="house",
        position=(2, 3),
        rooms=generate_house_rooms(rng, "House_A7DO")
    )
    world.buildings[main_house.name] = main_house

    # Neighbours
    used = {main_house.position}
    for i in range(1, 11):
        # find a free coordinate
        while True:
            pos = (rng.randint(0, world.grid_size[0]-1), rng.randint(0, world.grid_size[1]-1))
            if pos not in used:
                used.add(pos)
                break
        b = Building(
            name=f"Neighbour_{i}",
            kind="house",
            position=pos,
            rooms=generate_house_rooms(rng, f"Neighbour_{i}")
        )
        world.buildings[b.name] = b

    # Park + Street anchor
    park = Building(name="Park", kind="park", position=(6, 2), rooms={})
    street = Building(name="Street", kind="street", position=(4, 3), rooms={})
    world.buildings[park.name] = park
    world.buildings[street.name] = street

    # Simple street segments (cosmetic)
    world.streets.append((main_house.position, street.position))
    world.streets.append((street.position, park.position))

    return world

def ascii_map(world: WorldMap) -> str:
    w, h = world.grid_size
    grid = [[" ." for _ in range(w)] for __ in range(h)]
    for name, b in world.buildings.items():
        x, y = b.position
        token = "H"
        if b.kind == "park":
            token = "P"
        elif b.kind == "street":
            token = "S"
        elif name.startswith("Neighbour_"):
            token = "N"
        elif name == "House_A7DO":
            token = "A"
        grid[y][x] = f" {token}"
    # flip y for display (optional) – keep simple
    lines = ["".join(row) for row in grid]
    return "\n".join(lines)