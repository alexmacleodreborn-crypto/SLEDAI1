from world_frame.event_generator import EventGenerator
from world_frame.experience_controller import ExperienceController


class WorldController:
    def __init__(self):
        self.event_gen = EventGenerator()
        self.experience = ExperienceController()

    def generate_birth_experience(self):
        """
        High-intensity sensory burst.
        """
        return self.experience.birth_sequence()

    def generate_day_events(self, day: int, location: str, n_events: int):
        """
        Normal waking experiences.
        """
        return self.event_gen.generate(
            day=day,
            location=location,
            n_events=n_events,
        )