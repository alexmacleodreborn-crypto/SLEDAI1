# a7do/world.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random


# =========================
# CAGE BOUNDS (Observer)
# =========================

@dataclass
class CageBounds:
    min_x: int = -5
    max_x: int = 15
    min_y: int = -5
    max_y: int = 15

    def width(self) -> int:
        return self.max_x - self.min_x + 1

    def height(self) -> int:
        return self.max_y - self.min_y + 1


# =========================
# PLACES & BOTS
# =========================

@dataclass
class Place:
    place_id: str
    label: str
    kind: str
    pos_xy: Tuple[int, int]
    sensory: Dict[str, str] = field(default_factory=dict)


@dataclass
class BotState:
    name: str
    home_place: str
    state: str = "at_home"
    location: str = ""
    last_seen_day: int = -1


@dataclass
class WorldState:
    seed: int = 0
    places: Dict[str, Place] = field(default_factory=dict)
    routes: Dict[str, List[str]] = field(default_factory=dict)
    bots: Dict[str, BotState] = field(default_factory=dict)

    # Observer-only logs
    last_bot_movements: List[dict] = field(default_factory=list)

    def add_place(self, place: Place):
        self.places[place.place_id] = place
        self.routes.setdefault(place.place_id, [])

    def link(self, a: str, b: str):
        self.routes.setdefault(a, [])
        self.routes.setdefault(b, [])
        if b not in self.routes[a]:
            self.routes[a].append(b)
        if a not in self.routes[b]:
            self.routes[b].append(a)

    def get_sensory(self, place_id: str) -> Dict[str, str]:
        p = self.places.get(place_id)
        return dict(p.sensory) if p else {}

    def get_route(self, a: str, b: str) -> List[str]:
        if a == b:
            return [a]
        if b in self.routes.get(a, []):
            return [a, b]
        for mid in self.routes.get(a, []):
            if b in self.routes.get(mid, []):
                return [a, mid, b]
        return [a, b]


# =========================
# WORLD GENERATION
# =========================

def generate_world(seed: int = 7) -> WorldState:
    rng = random.Random(seed)
    w = WorldState(seed=seed)

    # Core places
    w.add_place(Place(
        "hospital", "City Hospital", "hospital", (0, 0),
        sensory={"smell": "antiseptic", "sound": "voices", "vision": "bright lights"}
    ))

    w.add_place(Place(
        "park", "Central Park", "park", (3, 1),
        sensory={"smell": "grass", "sound": "birds", "vision": "open sky"}
    ))

    w.add_place(Place(
        "shops", "Local Shops", "shops", (2, -1),
        sensory={"smell": "food", "sound": "chatter", "vision": "colourful shelves"}
    ))

    # Home & street
    w.add_place(Place(
        "street_main", "Main Street", "street", (1, 0),
        sensory={"sound": "traffic", "vision": "houses"}
    ))

    w.add_place(Place(
        "house_a7do", "A7DO Home", "home", (1, 1),
        sensory={"sound": "home quiet", "smell": "clean fabric"}
    ))

    w.add_place(Place(
        "bedroom_a7do", "A7DO Bedroom", "room", (1, 2),
        sensory={"sound": "muffled", "smell": "bedding"}
    ))

    # Links
    w.link("hospital", "street_main")
    w.link("street_main", "park")
    w.link("street_main", "shops")
    w.link("street_main", "house_a7do")
    w.link("house_a7do", "bedroom_a7do")

    # Neighbour houses
    for i in range(1, 11):
        pid = f"house_{i}"
        w.add_place(Place(
            pid, f"House {i}", "home", (1 + i, 1),
            sensory={"sound": "neighbour noise", "vision": "front door"}
        ))
        w.link("street_main", pid)

    # Bots
    w.bots["Mum"] = BotState("Mum", "house_a7do", location="house_a7do")
    w.bots["Dad"] = BotState("Dad", "house_a7do", location="house_a7do")
    w.bots["Sister"] = BotState("Sister", "house_a7do", location="house_a7do")
    w.bots["Lucy"] = BotState("Lucy", "house_7", location="house_7")
    w.bots["Millie"] = BotState("Millie", "house_7", location="house_7")

    return w


# =========================
# ASCII MAP (Observer)
# =========================

def ascii_map(world: WorldState, bounds: CageBounds) -> str:
    """
    Observer-only symbolic map.
    A7DO never sees this.
    """
    grid = [[" ." for _ in range(bounds.width())]
            for _ in range(bounds.height())]

    def place_char(kind: str) -> str:
        return {
            "hospital": " H",
            "park": " P",
            "shops": " S",
            "home": " O",
            "room": " R",
            "street": " =",
        }.get(kind, " ?")

    for place in world.places.values():
        x, y = place.pos_xy
        gx = x - bounds.min_x
        gy = bounds.max_y - y
        if 0 <= gx < bounds.width() and 0 <= gy < bounds.height():
            grid[gy][gx] = place_char(place.kind)

    return "\n".join("".join(row) for row in grid)