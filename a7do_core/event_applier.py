from a7do_core.world_state import WorldState
from a7do_core.events import ExperienceEvent


SENSORY_CHANNELS = {"sound", "light", "touch", "smell", "taste", "motion"}


def apply_event(event: ExperienceEvent, world: WorldState):
    """
    The ONLY place allowed to mutate WorldState from an ExperienceEvent.
    No inference, no meaning.
    """
    if world.frozen:
        raise RuntimeError("WorldState is frozen during sleep replay")

    world.day = event.day
    world.time += float(event.duration)
    world.location = event.place

    world.event_history.append(event.kind)

    # Raw accumulation by channel (channel intensity = 0.1 per token)
    for tag, values in (event.tags or {}).items():
        if tag in SENSORY_CHANNELS:
            world.body_state[tag] = world.body_state.get(tag, 0.0) + 0.1 * len(values)