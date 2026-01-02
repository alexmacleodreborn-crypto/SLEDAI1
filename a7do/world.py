# a7do/world.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import random


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

    # Observer-only logs (A7DO doesn't "know" these unless present)
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
        # Symbolic: direct hop if linked; else naive 2-hop search
        if a == b:
            return [a]
        if b in self.routes.get(a, []):
            return [a, b]
        for mid in self.routes.get(a, []):
            if b in self.routes.get(mid, []):
                return [a, mid, b]
        return [a, b]


def generate_world(seed: int = 7) -> WorldState:
    rng = random.Random(seed)
    w = WorldState(seed=seed)

    # Core places
    w.add_place(Place("hospital", "City Hospital", "hospital", (0, 0),
                      sensory={"smell": "antiseptic", "sound": "voices", "vision": "bright lights"}))
    w.add_place(Place("park", "Central Park", "park", (3, 1),
                      sensory={"smell": "grass", "sound": "birds", "vision": "open sky"}))
    w.add_place(Place("shops", "Local Shops", "shops", (2, -1),
                      sensory={"smell": "food", "sound": "chatter", "vision": "colourful shelves"}))

    # Services (observer-only realism)
    for sid, label in [
        ("groceries", "Groceries"),
        ("barbers", "Barbers"),
        ("dentist", "Dentist"),
        ("optician", "Optician"),
        ("doctors", "Doctors"),
    ]:
        w.add_place(Place(sid, label, "service", (2 + rng.randint(-1, 1), -2 + rng.randint(-1, 1)),
                          sensory={"sound": "indoor hum", "vision": "fluorescent", "smell": "mixed"}))
        w.link("shops", sid)

    # Home street & houses
    w.add_place(Place("street_main", "Main Street", "street", (1, 0),
                      sensory={"sound": "traffic", "vision": "houses"}))
    w.add_place(Place("house_a7do", "A7DO Home", "home", (1, 1),
                      sensory={"sound": "home quiet", "smell": "clean fabric"}))
    w.add_place(Place("bedroom_a7do", "A7DO Bedroom", "room", (1, 2),
                      sensory={"sound": "muffled", "smell": "bedding"}))

    w.link("hospital", "street_main")
    w.link("street_main", "park")
    w.link("street_main", "shops")
    w.link("street_main", "house_a7do")
    w.link("house_a7do", "bedroom_a7do")

    # Neighbours: 10 houses (IDs: house_1..house_10)
    for i in range(1, 11):
        pid = f"house_{i}"
        w.add_place(Place(pid, f"House {i}", "home", (1 + i, 1),
                          sensory={"sound": "neighbour noise", "vision": "front door"}))
        w.link("street_main", pid)

    # Define bots (people) (simple)
    w.bots["Mum"] = BotState("Mum", home_place="house_a7do", location="house_a7do")
    w.bots["Dad"] = BotState("Dad", home_place="house_a7do", location="house_a7do")
    w.bots["Sister"] = BotState("Sister", home_place="house_a7do", location="house_a7do")

    # Neighbour 7: Lucy (you referenced)
    w.bots["Lucy"] = BotState("Lucy", home_place="house_7", location="house_7")
    # Neighbour dog (Millie)
    w.bots["Millie"] = BotState("Millie", home_place="house_7", location="house_7", state="at_home")

    return w


def tick_bot_routines(world: WorldState, day: int) -> List[dict]:
    """
    Observer-only background movement tick.
    DOES NOT create A7DO events.
    Just logs where bots go today.
    """
    rng = random.Random(world.seed * 1000 + day)
    moves = []

    def move(bot: BotState, to_place: str, state: str):
        prev = bot.location
        bot.location = to_place
        bot.state = state
        moves.append({"day": day, "bot": bot.name, "from": prev, "to": to_place, "state": state})

    # Lucy: often walks dog to park
    lucy = world.bots.get("Lucy")
    millie = world.bots.get("Millie")
    if lucy:
        if rng.random() < 0.6:
            move(lucy, "park", "walking_dog")
            if millie:
                move(millie, "park", "walking_with_owner")
        else:
            move(lucy, lucy.home_place, "at_home")
            if millie:
                move(millie, millie.home_place, "at_home")

    # Dad: simple "out then home" (work is abstract)
    dad = world.bots.get("Dad")
    if dad:
        if rng.random() < 0.5:
            move(dad, "street_main", "driving")
        else:
            move(dad, "house_a7do", "at_home")

    # Mum: shops/park sometimes
    mum = world.bots.get("Mum")
    if mum:
        r = rng.random()
        if r < 0.35:
            move(mum, "shops", "at_shops")
        elif r < 0.60:
            move(mum, "park", "at_park")
        else:
            move(mum, "house_a7do", "at_home")

    world.last_bot_movements = moves
    return moves