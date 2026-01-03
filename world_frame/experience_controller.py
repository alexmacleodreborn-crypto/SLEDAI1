# world_frame/experience_controller.py

class ExperienceController:
    """
    Controls which life phase A7DO is in.
    """

    PHASES = [
        "pre_birth",
        "birth",
        "hospital",
        "journey_home",
        "home_day",
        "sleep",
    ]

    def __init__(self):
        self.phase = "pre_birth"

    def advance(self):
        idx = self.PHASES.index(self.phase)
        if idx < len(self.PHASES) - 1:
            self.phase = self.PHASES[idx + 1]

    def is_phase(self, name: str) -> bool:
        return self.phase == name