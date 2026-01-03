from world_frame.places import HOSPITAL


class ExperienceController:
    def birth_sequence(self):
        return [
            {"type": "PRESSURE", "target": "chest", "intensity": 1.0},
            {"type": "PRESSURE", "target": "head", "intensity": 0.9},
            {"type": "LIQUID", "target": "skin"},
            {"type": "SOUND", "value": "scream", "loudness": 1.0},
            {"type": "LIGHT", "brightness": 1.0},
            {"type": "AIR", "cold": True},
            {"type": "BREATH", "first": True},
            {"type": "VOICE", "source": "mother"},
            {"type": "TOUCH", "source": "hands"},
        ]