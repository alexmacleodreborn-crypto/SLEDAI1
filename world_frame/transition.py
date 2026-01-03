# world_frame/transition.py

from world_frame.world_state import WorldState, WorldEvent


def apply_transition(
    world: WorldState,
    to_place: str,
    description: str = "",
):
    """
    Apply a physical transition in the world.
    This is objective movement, not perception.
    """

    world.current_place = to_place

    world.events.append(
        WorldEvent(
            time=world.time,
            place=to_place,
            description=description or f"Transitioned to {to_place}",
            tags=["transition", "movement"],
        )
    )