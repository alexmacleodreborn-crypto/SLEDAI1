# world_frame/transitions.py

class Transition:
    def __init__(self, name: str, motion_level: float):
        self.name = name
        self.motion_level = motion_level  # feeds sensory tags

    def __repr__(self):
        return self.name


# Allowed transitions
CARRIED = Transition("carried", motion_level=0.4)
CAR_RIDE = Transition("car", motion_level=0.8)
WALKED = Transition("walked", motion_level=0.6)