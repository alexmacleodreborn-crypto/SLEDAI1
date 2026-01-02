from world_frame.world_state import WorldState
from world_frame.places import hospital_birth_suite, family_home, bedroom

class WorldController:
    def __init__(self):
        self.state = WorldState()

    def initialize_birth_world(self):
        birth_room = hospital_birth_suite()
        self.state.places[birth_room["id"]] = birth_room
        self.state.current_place_id = birth_room["id"]
        self.state.current_day = 0

    def add_home_world(self):
        home = family_home()
        bed = bedroom()
        self.state.places[home["id"]] = home
        self.state.places[bed["id"]] = bed

    def move_entity(self, entity_id: str, place_id: str):
        self.state.presence[entity_id] = place_id
        self.state.current_place_id = place_id

    def advance_day(self):
        self.state.current_day += 1