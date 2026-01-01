from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid

# ---------------------------
# Core Entity Profiles
# ---------------------------

@dataclass
class PersonProfile:
    name: str
    role: str  # mum, dad, neighbour, self
    age: int
    hair: str
    eyes: str
    features: List[str] = field(default_factory=list)

    # relationships by type → list of entity names
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

    # ownership / attachment
    owner: Optional[str] = None
    relationships: Dict[str, List[str]] = field(default_factory=dict)

    def set_owner(self, owner_name: str):
        self.owner = owner_name
        self.relationships.setdefault("owner", [])
        if owner_name not in self.relationships["owner"]:
            self.relationships["owner"].append(owner_name)


@dataclass
class ObjectProfile:
    """
    Represents a *type* of object (ball, tool, swing).
    Instances are tracked separately.
    """
    name: str
    category: str  # toy, tool, container, furniture
    colour: Optional[str] = None
    shape: Optional[str] = None
    affordances: List[str] = field(default_factory=list)

    # containment semantics (toolbox contains tools)
    container_of: Optional[str] = None


@dataclass
class ObjectInstance:
    """
    Represents a *specific instance* of an object.
    """
    instance_id: str
    object_type: str  # name of ObjectProfile
    colour: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    status: str = "present"  # present | gone | broken

# ---------------------------
# World Profile Registry
# ---------------------------

class WorldProfiles:
    """
    Observer-defined world truth.
    A7DO may EXPERIENCE this world but may not invent it.
    """

    def __init__(self):
        self.people: Dict[str, PersonProfile] = {}
        self.animals: Dict[str, AnimalProfile] = {}
        self.objects: Dict[str, ObjectProfile] = {}

        # concrete object instances (balls, tools, swings)
        self.object_instances: Dict[str, ObjectInstance] = {}

        # background "what parents know" – not directly known by A7DO
        self.parent_knowledge: Dict[str, List[str]] = {}

    # ---------------------------
    # Validation helpers
    # ---------------------------

    def has_parents(self) -> bool:
        roles = {p.role.lower() for p in self.people.values()}
        return ("mum" in roles) and ("dad" in roles)

    def person_exists(self, name: str) -> bool:
        return name in self.people

    def animal_exists(self, name: str) -> bool:
        return name in self.animals

    def object_exists(self, name: str) -> bool:
        return name in self.objects

    # ---------------------------
    # Relationship helpers
    # ---------------------------

    def relate_person_to_person(self, a: str, rel: str, b: str):
        if a in self.people and b in self.people:
            self.people[a].add_relationship(rel, b)

    def assign_pet(self, pet_name: str, owner_name: str):
        if pet_name in self.animals and owner_name in self.people:
            self.animals[pet_name].set_owner(owner_name)
            self.people[owner_name].add_relationship("pet", pet_name)

    # ---------------------------
    # Object instance helpers
    # ---------------------------

    def create_object_instance(
        self,
        object_type: str,
        colour: Optional[str] = None,
        location: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> ObjectInstance:
        if object_type not in self.objects:
            raise ValueError(f"Unknown object type: {object_type}")

        iid = str(uuid.uuid4())[:8]
        inst = ObjectInstance(
            instance_id=iid,
            object_type=object_type,
            colour=colour,
            location=location,
            owner=owner,
        )
        self.object_instances[iid] = inst
        return inst

    def find_instances(self, object_type: str) -> List[ObjectInstance]:
        return [
            i for i in self.object_instances.values()
            if i.object_type == object_type and i.status == "present"
        ]

    # ---------------------------
    # Observer snapshot
    # ---------------------------

    def snapshot(self):
        return {
            "people": {
                p.name: {
                    "role": p.role,
                    "relationships": p.relationships
                }
                for p in self.people.values()
            },
            "animals": {
                a.name: {
                    "species": a.species,
                    "owner": a.owner
                }
                for a in self.animals.values()
            },
            "objects": {
                o.name: {
                    "category": o.category,
                    "colour": o.colour,
                    "affordances": o.affordances
                }
                for o in self.objects.values()
            },
            "object_instances": {
                i.instance_id: {
                    "type": i.object_type,
                    "colour": i.colour,
                    "location": i.location,
                    "owner": i.owner,
                    "status": i.status
                }
                for i in self.object_instances.values()
            },
            "parent_knowledge_keys": list(self.parent_knowledge.keys()),
        }