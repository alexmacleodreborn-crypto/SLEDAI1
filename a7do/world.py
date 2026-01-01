from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random

@dataclass
class CageBounds:
    x_min: int = -50
    x_max: int = 50
    y_min: int = -50
    y_max: int = 50
    z_min: int = -2
    z_max: int = 10

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
class Place:
    place_id: str
    kind: str  # hospital, house, park, shop, street
    name: str
    pos_xyz: Tuple[float, float, float]
    rooms: Dict[str, Room] = field(default_factory=dict)
    meta: Dict[str, str] = field(default_factory=dict)

@dataclass
class WorldMap:
    seed: int
    cage: CageBounds = field(default_factory=CageBounds)
    places: Dict[str, Place] = field(default_factory=dict)
    streets: List[Tuple[str, str]] = field(default_factory=list)  # adjacency edges

    def add_place(self, place: Place):
        self.places[place.place_id] = place

    def connect(self, a_id: str, b_id: str):
        self.streets.append((a_id, b_id))

WALLS = ["cream", "light blue", "soft green", "white", "light grey", "warm beige"]
DOOR_COLOURS = ["blue", "red", "green", "black", "white", "yellow", "orange", "purple"]

def _rdim(rng, a, b):
    return round(rng.uniform(a, b), 2)

def generate_home_rooms(rng) -> Dict[str, Room]:
    def mk(name, w_rng, l_rng, fixtures, sound, smell):
        return Room(
            name=name,
            width_m=_rdim(rng, *w_rng),
            length_m=_rdim(rng, *l_rng),
            wall_colour=rng.choice(WALLS),
            windows=rng.randint(0, 2),
            baseline_sound=sound,
            baseline_smell=smell,
            fixtures=fixtures,
        )

    return {
        "hall": mk("hall", (2.0, 3.5), (3.0, 6.0), ["doorway", "coat hook"], "house hum", "neutral"),
        "living_room": mk("living_room", (2.8, 5.5), (3.0, 6.0), ["sofa", "table", "lamp"], "quiet", "neutral"),
        "kitchen": mk("kitchen", (2.5, 5.0), (2.5, 5.5), ["cupboard", "sink", "table"], "clink", "food"),
        "bathroom": mk("bathroom", (1.8, 3.0), (1.8, 3.5), ["toilet", "sink"], "fan", "soap"),
        "bedroom_child": mk("bedroom_child", (2.5, 4.5), (2.5, 5.0), ["bed", "curtains", "toy box"], "quiet", "clean"),
        "bedroom_parent": mk("bedroom_parent", (2.6, 5.0), (2.6, 5.5), ["bed", "wardrobe", "curtains"], "quiet", "clean"),
        "bedroom_sister": mk("bedroom_sister", (2.4, 4.2), (2.4, 4.8), ["bed", "books", "curtains"], "quiet", "clean"),
    }

def generate_world(seed: int, neighbour_count: int = 20) -> WorldMap:
    rng = random.Random(seed)
    world = WorldMap(seed=seed)

    # Anchor: Hospital at centre
    hospital = Place(
        place_id="hospital_cwh",
        kind="hospital",
        name="City World Hospital",
        pos_xyz=(0.0, 0.0, 0.0),
        rooms={
            "delivery_room": Room(
                name="delivery_room",
                width_m=6.0, length_m=6.0,
                wall_colour="white",
                windows=0,
                baseline_sound="echo voices",
                baseline_smell="clean chemical",
                fixtures=["lights", "bed", "trolley"]
            )
        },
        meta={"street_name": "Hospital Street"}
    )
    world.add_place(hospital)

    park = Place(place_id="park_01", kind="park", name="Central Park", pos_xyz=(18.0, 6.0, 0.0), meta={"street_name": "Park Lane"})
    shops = Place(place_id="shops_01", kind="shop", name="Corner Shops", pos_xyz=(12.0, -10.0, 0.0), meta={"street_name": "Market Road"})
    world.add_place(park)
    world.add_place(shops)

    home_street = Place(place_id="street_home", kind="street", name="Home Street", pos_xyz=(24.0, -2.0, 0.0), meta={"street_name": "Home Street"})
    world.add_place(home_street)

    a7do_home = Place(
        place_id="house_a7do",
        kind="house",
        name="A7DO Home",
        pos_xyz=(28.0, -2.0, 0.0),
        rooms=generate_home_rooms(rng),
        meta={
            "door_colour": "blue",
            "front_garden": "yes",
            "back_garden": "yes",
            "levels": "2",
            "street_name": "Home Street",
            "door_number": "1"
        }
    )
    world.add_place(a7do_home)

    for i in range(1, neighbour_count + 1):
        door_no = str(i + 1)
        x = 28.0 + (i * 2.0)
        y = -2.0 + (0.0 if i % 2 == 0 else 1.5)
        place = Place(
            place_id=f"house_n_{door_no}",
            kind="house",
            name=f"House {door_no}",
            pos_xyz=(x, y, 0.0),
            rooms=generate_home_rooms(rng),
            meta={
                "door_number": door_no,
                "door_colour": rng.choice(DOOR_COLOURS),
                "street_name": "Home Street",
                "levels": "2",
                "front_garden": "yes",
                "back_garden": "yes",
                "odd_has_car": "yes" if int(door_no) % 2 == 1 else "no",
                "even_has_dog": "yes" if int(door_no) % 2 == 0 else "no",
            }
        )
        world.add_place(place)

    world.connect("hospital_cwh", "park_01")
    world.connect("park_01", "shops_01")
    world.connect("shops_01", "street_home")
    world.connect("street_home", "house_a7do")

    for i in range(2, neighbour_count + 2):
        world.connect("street_home", f"house_n_{i}")

    return world

def ascii_map(world: WorldMap) -> str:
    lines = []
    lines.append("World Places:")
    for pid, p in world.places.items():
        x, y, z = p.pos_xyz
        lines.append(f"- {pid:12s} | {p.kind:8s} | {p.name:20s} @ ({x:5.1f},{y:5.1f},{z:3.1f})")
    lines.append("")
    lines.append("Connections:")
    for a, b in world.streets[:50]:
        lines.append(f"- {a} -> {b}")
    if len(world.streets) > 50:
        lines.append(f"... {len(world.streets)-50} more")
    return "\n".join(lines)