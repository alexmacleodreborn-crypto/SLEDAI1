from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
import uuid

# ---------------------------
# Core Profiles
# ---------------------------

@dataclass
class PersonProfile:
    name: str
    role: str  # mum, dad, sister, neighbour, self
    age: int
    hair: str
    eyes: str
    features: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)

    def add_relationship(self, rel: str, target: str):
        self.relationships.setdefault(rel, [])
        if target not in self.relationships[rel]:
            self.relationships[rel].append(target)

@dataclass
class AnimalProfile:
    name: str
    species: str
    temperament: str = "calm"
    sounds: List[str] = field(default_factory=list)
    owner: Optional[str] = None

@dataclass
class ObjectProfile:
    name: str
    category: str  # toy, tool, container, furniture
    colour: Optional[str] = None
    shape: Optional[str] = None
    affordances: List[str] = field(default_factory=list)
    container_of: Optional[str] = None  # toolbox contains tool etc.

@dataclass
class InteractionRecord:
    person_name: str
    last_outcome: str  # calm | cried | reached | withdrew
    last_day: int
    notes: List[str] = field(default_factory=list)

# ---------------------------
# Registry
# ---------------------------

class WorldProfiles:
    """
    Observer-defined truth (allowed reality).
    A7DO experiences it; does not invent it.
    """
    def __init__(self):
        self.people: Dict[str, PersonProfile] = {}
        self.animals: Dict[str, AnimalProfile] = {}
        self.objects: Dict[str, ObjectProfile] = {}

        # background knowledge for planner only (parents)
        self.parent_knowledge: Dict[str, List[str]] = {}

        # interaction memory (transaction log) keyed by person
        self.interactions: Dict[str, InteractionRecord] = {}

        # mapping door->family ids for neighbours
        self.neighbour_families: Dict[str, Dict[str, str]] = {}

    def has_parents(self) -> bool:
        roles = {p.role.lower() for p in self.people.values()}
        return ("mum" in roles) and ("dad" in roles)

    def snapshot(self):
        return {
            "people": {k: {"role": v.role, "age": v.age, "hair": v.hair, "eyes": v.eyes, "relationships": v.relationships} for k, v in self.people.items()},
            "animals": {k: {"species": v.species, "owner": v.owner} for k, v in self.animals.items()},
            "objects": {k: {"category": v.category, "colour": v.colour, "shape": v.shape, "affordances": v.affordances} for k, v in self.objects.items()},
            "parent_knowledge_keys": list(self.parent_knowledge.keys()),
            "interactions": {k: {"last_outcome": v.last_outcome, "last_day": v.last_day} for k, v in self.interactions.items()},
            "neighbour_families_count": len(self.neighbour_families),
        }

    # ---------------------------
    # Relationships
    # ---------------------------

    def assign_pet(self, pet_name: str, owner_name: str):
        if pet_name in self.animals and owner_name in self.people:
            self.animals[pet_name].owner = owner_name
            self.people[owner_name].add_relationship("pet", pet_name)

    def set_interaction(self, person_name: str, outcome: str, day: int, notes: Optional[List[str]] = None):
        notes = notes or []
        self.interactions[person_name] = InteractionRecord(person_name=person_name, last_outcome=outcome, last_day=day, notes=notes)

    # ---------------------------
    # Neighbour generator
    # ---------------------------

    def generate_neighbours(self, seed: int, door_numbers: List[str]):
        rng = random.Random(seed)

        first_names_m = ["James", "Craig", "Tom", "Mark", "Owen", "Liam", "Noah", "Leo", "Finn", "Alex"]
        first_names_f = ["Sarah", "Mags", "Emma", "Sophie", "Zoe", "Ava", "Mia", "Ella", "Grace", "Lucy"]
        hair = ["brown", "blonde", "black", "red", "grey"]
        eyes = ["blue", "green", "brown", "hazel"]

        # pick 3 special families: single mum, single dad, blended
        specials = rng.sample(door_numbers, k=min(3, len(door_numbers)))
        special_map = {}
        if len(specials) >= 1: special_map[specials[0]] = "single_mum"
        if len(specials) >= 2: special_map[specials[1]] = "single_dad"
        if len(specials) >= 3: special_map[specials[2]] = "blended"

        for door in door_numbers:
            style = special_map.get(door, "standard")

            dad_name = f"{rng.choice(first_names_m)}_{door}_Dad"
            mum_name = f"{rng.choice(first_names_f)}_{door}_Mum"
            c1 = f"{rng.choice(first_names_m)}_{door}_Boy"
            c2 = f"{rng.choice(first_names_f)}_{door}_Girl"

            fam = {"style": style}

            if style == "single_mum":
                # mum + two kids; dad exists as concept but not present
                self.people[mum_name] = PersonProfile(mum_name, "neighbour_mum", rng.randint(24, 45), rng.choice(hair), rng.choice(eyes), ["tired smile"])
                self.people[c1] = PersonProfile(c1, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                self.people[c2] = PersonProfile(c2, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                fam.update({"mum": mum_name, "dad": "unknown_dad_card", "child1": c1, "child2": c2})

            elif style == "single_dad":
                self.people[dad_name] = PersonProfile(dad_name, "neighbour_dad", rng.randint(24, 45), rng.choice(hair), rng.choice(eyes), ["gentle voice"])
                self.people[c1] = PersonProfile(c1, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                self.people[c2] = PersonProfile(c2, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                fam.update({"dad": dad_name, "mum": "unknown_mum_card", "child1": c1, "child2": c2})

            elif style == "blended":
                # step dad + mum + bio dad exists elsewhere; one child from mum, one from dad
                step_dad = f"{rng.choice(first_names_m)}_{door}_StepDad"
                bio_dad = f"{rng.choice(first_names_m)}_{door}_BioDad"
                self.people[mum_name] = PersonProfile(mum_name, "neighbour_mum", rng.randint(24, 45), rng.choice(hair), rng.choice(eyes), ["confident"])
                self.people[step_dad] = PersonProfile(step_dad, "neighbour_stepdad", rng.randint(24, 50), rng.choice(hair), rng.choice(eyes), ["friendly"])
                self.people[c1] = PersonProfile(c1, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                self.people[c2] = PersonProfile(c2, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                fam.update({"mum": mum_name, "stepdad": step_dad, "biodad": bio_dad, "child1": c1, "child2": c2})

            else:
                self.people[dad_name] = PersonProfile(dad_name, "neighbour_dad", rng.randint(24, 50), rng.choice(hair), rng.choice(eyes), ["hello wave"])
                self.people[mum_name] = PersonProfile(mum_name, "neighbour_mum", rng.randint(24, 50), rng.choice(hair), rng.choice(eyes), ["warm smile"])
                self.people[c1] = PersonProfile(c1, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                self.people[c2] = PersonProfile(c2, "neighbour_child", rng.randint(4, 10), rng.choice(hair), rng.choice(eyes), [])
                fam.update({"dad": dad_name, "mum": mum_name, "child1": c1, "child2": c2})

            self.neighbour_families[door] = fam