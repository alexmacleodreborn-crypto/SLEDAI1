from typing import List
from a7do.events import ExperienceEvent


class CaregiverFlow:
    def __init__(self, start_place: str = "hospital"):
        self.start_place = start_place

    def build_day(self, day: int, n_events: int = 10) -> List[ExperienceEvent]:
        events: List[ExperienceEvent] = []

        place = self.start_place if day == 0 else "home"

        for i in range(n_events):
            kind = "care"
            notes = "routine care"

            if day == 0 and i == 0:
                kind = "birth"
                place = "hospital"
                notes = "birth"

            elif day == 0 and i == n_events // 2:
                kind = "travel"
                place = "home"
                notes = "journey home"

            elif i == n_events - 1:
                kind = "sleep"
                place = "bedroom"
                notes = "sleep"

            events.append(
                ExperienceEvent(
                    day=day,
                    index=i,
                    kind=kind,
                    place=place,
                    people_present=["Mum", "Dad"],
                    notes=notes,
                )
            )

        return events