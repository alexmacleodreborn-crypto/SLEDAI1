from a7do_core.events import ExperienceEvent
from a7do_core.world_state import WorldState
from a7do_core.perceived_world_state import PerceivedWorldState

SENSORY_CHANNELS = {"sound", "light", "touch", "smell", "taste", "motion"}


def apply_event(
    event: ExperienceEvent,
    world: WorldState,
    perceived: PerceivedWorldState | None = None,
):
    """
    Applies a single ExperienceEvent to A7DO.
    No inference. No semantics. No shortcuts.
    """

    if world.frozen:
        raise RuntimeError("Cannot apply live events while world is frozen (sleep replay)")

    # Update world clock
    world.day = event.day
    world.time += float(event.duration)

    # Place token only (string or Place object)
    if hasattr(event.place, "name"):
        world.location = event.place.name
    else:
        world.location = event.place

    world.event_history.append(event.kind)

    # Raw body accumulation
    for tag, values in (event.tags or {}).items():
        if tag in SENSORY_CHANNELS:
            world.body_state[tag] = world.body_state.get(tag, 0.0) + 0.1 * len(values)

    # Subjective place familiarity (if provided)
    if perceived is not None:
        affect = (event.tags or {}).get("affect", [])
        perceived.update_from_event(
            place=world.location or "",
            day=world.day,
            duration=float(event.duration),
            affect=affect,
        )