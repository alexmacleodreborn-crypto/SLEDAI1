from a7do.world import WorldState
from a7do.events import ExperienceEvent


def apply_event_to_world(world: WorldState, ev: ExperienceEvent):
    # Time
    world.current_day = ev.day
    world.current_event_index = ev.index

    # Location
    if ev.place:
        world.a7do_location = ev.place

    # Movement
    if ev.movement:
        world.last_movement = {
            "from": ev.movement.get("from"),
            "to": ev.movement.get("to"),
            "mode": ev.movement.get("mode"),
            "day": ev.day,
            "event": ev.index,
        }
        if "posture" in ev.movement:
            world.a7do_posture = ev.movement["posture"]

    # Transport
    if ev.transport:
        world.last_transport = ev.transport

    # People present
    for name in ev.people_present:
        if name in world.bots:
            bot = world.bots[name]
            bot.location = world.a7do_location
            bot.last_seen_day = ev.day
            bot.last_seen_event = ev.index

    # Sleep
    if ev.kind == "sleep":
        world.last_sleep_location = world.a7do_location
        world.last_sleep_day = ev.day

    # 🔑 CRITICAL: persist event for observer
    world.event_log.append({
        "day": ev.day,
        "index": ev.index,
        "kind": ev.kind,
        "place": ev.place,
        "notes": ev.notes,
    })