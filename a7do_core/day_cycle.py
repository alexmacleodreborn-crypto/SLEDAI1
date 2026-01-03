from typing import List

from a7do_core.a7do_state import A7DOState
from a7do_core.event_applier import apply_event
from a7do_core.sleep import run_sleep

from world_frame.world_controller import WorldController
from world_frame.transition import apply_transition


class DayCycle:
    def __init__(self, a7do: A7DOState, world: WorldController):
        self.a7do = a7do
        self.world = world

    def initialise_if_needed(self):
        """
        Birth happens here. Exactly once.
        """
        if self.a7do.birthed:
            return []

        # Ask the world for the birth experience
        birth_events = self.world.generate_birth_experience()

        for ev in birth_events:
            apply_event(self.a7do, ev)

        self.a7do.birthed = True
        self.a7do.current_place = "Hospital"
        self.a7do.internal_log.append("Birth completed")

        return birth_events

    def run_day(self, n_events: int = 10):
        """
        Runs one waking block of experience.
        """
        events = self.world.generate_day_events(
            day=self.a7do.day_index,
            location=self.a7do.current_place,
            n_events=n_events,
        )

        for ev in events:
            apply_event(self.a7do, ev)

        return events

    def sleep(self):
        """
        Consolidation + learning happens here.
        """
        run_sleep(self.a7do)
        self.a7do.internal_log.append("Sleep complete")

    def advance_day(self):
        """
        Transition world + increment time.
        """
        apply_transition(self.a7do, self.world)
        self.a7do.day_index += 1
        self.a7do.internal_log.append(f"Day {self.a7do.day_index} started")