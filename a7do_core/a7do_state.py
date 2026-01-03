from a7do_core.perceived_world_state import PerceivedWorldState

class A7DOState:
    def __init__(self):
        self.birthed = False
        self.day_index = 0

        self.perceived_world = PerceivedWorldState()
        self.internal_log = []