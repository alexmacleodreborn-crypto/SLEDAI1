# a7do/day_cycle.py

from dataclasses import dataclass

DAY_BIRTH = "birth"
DAY_NORMAL = "normal"

PHASE_WAKE = "wake"
PHASE_ACTIVE = "active"
PHASE_SLEEP = "sleep"

@dataclass
class DayCycle:
    day_index: int = 0
    day_type: str = DAY_BIRTH
    phase: str = PHASE_WAKE
    birthed: bool = False

    def is_birth_day(self) -> bool:
        return self.day_type == DAY_BIRTH

    def begin_birth(self):
        self.birthed = True
        self.day_index = 0
        self.day_type = DAY_BIRTH
        self.phase = PHASE_ACTIVE

    def begin_new_day(self):
        self.day_index += 1
        self.day_type = DAY_NORMAL
        self.phase = PHASE_WAKE

    def wake(self):
        self.phase = PHASE_ACTIVE

    def sleep(self):
        self.phase = PHASE_SLEEP

    def advance_after_sleep(self):
        """
        Called once sleep consolidation finishes.
        """
        if self.day_type == DAY_BIRTH:
            # Birth day ends → normal life begins
            self.begin_new_day()
        else:
            # Normal next day
            self.begin_new_day()