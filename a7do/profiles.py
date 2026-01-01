from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class PersonProfile:
    name: str
    role: str  # mum, dad, neighbour
    age: int
    hair: str
    eyes: str
    features: List[str] = field(default_factory=list)

@dataclass
class AnimalProfile:
    name: str
    species: str
    temperament: str = "calm"
    sounds: List[str] = field(default_factory=list)

@dataclass
class ObjectProfile:
    name: str
    category: str  # toy, tool, container, furniture
    colour: Optional[str] = None
    shape: Optional[str] = None
    affordances: List[str] = field(default_factory=list)
    container_of: Optional[str] = None  # e.g. toolbox contains tool

class WorldProfiles:
    """
    Observer-defined entities (allowed reality).
    """
    def __init__(self):
        self.people: Dict[str, PersonProfile] = {}
        self.animals: Dict[str, AnimalProfile] = {}
        self.objects: Dict[str, ObjectProfile] = {}

        # background "what parents know" – stored as facts for schedule planning only
        self.parent_knowledge: Dict[str, List[str]] = {}

    def has_parents(self) -> bool:
        roles = {p.role.lower() for p in self.people.values()}
        return ("mum" in roles) and ("dad" in roles)

    def snapshot(self):
        return {
            "people": [f"{p.name} ({p.role})" for p in self.people.values()],
            "animals": [f"{a.name} ({a.species})" for a in self.animals.values()],
            "objects": [f"{o.name} ({o.category})" for o in self.objects.values()],
            "parent_knowledge_keys": list(self.parent_knowledge.keys()),
        }