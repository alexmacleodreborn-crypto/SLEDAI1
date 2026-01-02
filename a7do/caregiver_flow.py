# a7do/caregiver_flow.py

from typing import List
from a7do.events import ExperienceEvent


class CaregiverFlow:
    def __init__(self, start_place: str = "hospital"):
        self.start_place = start_place

    def build_day(self, day: int, n_events: int = 10) -> List[ExperienceEvent]:
        events: List[ExperienceEvent] = []

        for i in range(n_events):
            # --- Birth: ALWAYS day 0, event 0 ---
            if day == 0 and i == 0:
                events.append(
                    ExperienceEvent(
                        day=0,
                        index=0,
                        kind="birth",
                        place="hospital",
                        people_present=["Mum", "Dad"],
                        notes="A7DO birth event",
                    )
                )
                continue

            # --- Journey home ---
            if day == 0 and i == n_events // 2:
                events.append(
                    ExperienceEvent(
                        day=day,
                        index=i,
                        kind="travel",
                        place="home",
                        people_present=["Mum", "Dad"],
                        transport={"type": "car"},
                        notes="Journey home from hospital",
                    )
                )
                continue

            # --- Sleep ---
            if i == n_events - 1:
                events.append(
                    ExperienceEvent(
                        day=day,
                        index=i,
                        kind="sleep",
                        place="bedroom",
                        people_present=["Mum", "Dad"],
                        notes="Sleep",
                    )
                )
                continue

            # --- Default care ---
            events.append(
                ExperienceEvent(
                    day=day,
                    index=i,
                    kind="care",
                    place="hospital" if day == 0 else "home",
                    people_present=["Mum", "Dad"],
                    notes="Routine care",
                )
            )

        return events