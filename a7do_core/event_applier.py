# a7do_core/event_applier.py
from a7do_core.world_state import WorldState
from a7do_core.events import ExperienceEvent


def apply_event(event: ExperienceEvent, world: WorldState):
    """
    Apply an ExperienceEvent to the WorldState.

    This function MUST NOT:
    - infer meaning
    - extract schemas
    - teach language
    - modify knowledge structures
    """

    if world.frozen:
        raise RuntimeError("WorldState is frozen during sleep replay")

    # Temporal update
    world.day = event.day
    world.time += event.duration

    # Spatial update
    world.location = event.place

    # History
    world.event_history.append(event.kind)

    # Raw somatic accumulation from tags
    for tag, values in event.tags.items():
        # Each tag contributes minimally; no interpretation
        world.body_state[tag] = world.body_state.get(tag, 0.0) + (0.1 * len(values))