# a7do/event_applier.py
from a7do.world import WorldState
from a7do.events import ExperienceEvent


def apply_event_to_world(world: WorldState, ev: ExperienceEvent):
    """
    Apply the physical consequences of an event to the world.
    Observer-side only.
    """

    # Update A7DO location
    world.a7do_location = ev.place

    # Apply movement if present
    if ev.movement:
        world.last_movement = {
            "from": ev.movement.get("from"),
            "to": ev.movement.get("to"),
            "day": ev.day,
            "event": ev.index,
        }

    # Update bots present
    for name in ev.people_present:
        if name in world.bots:
            world.bots[name].location = ev.place
            world.bots[name].last_seen_day = ev.day