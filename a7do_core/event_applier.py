from a7do_core.perceived_world_state import PerceivedWorldState
from a7do_core.internal_log import log_internal


def apply_event(a7do, event):
    """
    Apply an EXPERIENCE event to A7DO.
    This never mutates the real world.
    """

    pw: PerceivedWorldState = a7do.perceived_world

    # Location awareness
    if event.place:
        pw.current_place = event.place
        log_internal(a7do, f"I am at {event.place}")

    # Sensory channels
    for sense, value in event.sensory.items():
        pw.senses[sense].append(value)
        log_internal(a7do, f"I sense {sense}: {value}")

    # Body changes
    if event.body:
        for part, state in event.body.items():
            a7do.body_local.update(part, state)
            log_internal(a7do, f"My {part} feels {state}")

    # Emotional / internal tags
    for tag in event.tags:
        pw.tags.add(tag)
        log_internal(a7do, f"Something happened: {tag}")