"""
event_applier.py

Observer-side reconciliation layer.

This module applies the *physical consequences* of ExperienceEvents
to the WorldState. It does NOT modify cognition, memory, or learning.

Authoritative rule:
Events describe experience.
WorldState describes objective reality.
"""

from typing import Optional

from a7do.world import WorldState
from a7do.events import ExperienceEvent


def apply_event_to_world(world: WorldState, ev: ExperienceEvent):
    """
    Apply a single ExperienceEvent to the WorldState.

    This updates:
    - A7DO physical location
    - A7DO posture / movement (if present)
    - Bot locations for people present
    - Last-known world time markers

    This function MUST be called exactly once per event.
    """

    # --- Update global time markers ---
    world.current_day = ev.day
    world.current_event_index = ev.index

    # --- Update A7DO location ---
    if ev.place:
        world.a7do_location = ev.place

    # --- Update A7DO movement / posture ---
    if ev.movement:
        world.last_movement = {
            "from": ev.movement.get("from"),
            "to": ev.movement.get("to"),
            "mode": ev.movement.get("mode"),
            "day": ev.day,
            "event": ev.index,
        }

        # Optional posture tracking
        posture = ev.movement.get("posture")
        if posture:
            world.a7do_posture = posture

    # --- Update people / bots present ---
    for person_name in ev.people_present:
        bot = world.bots.get(person_name)
        if bot:
            bot.location = world.a7do_location
            bot.last_seen_day = ev.day
            bot.last_seen_event = ev.index

    # --- Optional transport handling ---
    if ev.transport:
        world.last_transport = {
            "type": ev.transport.get("type"),
            "from": ev.transport.get("from"),
            "to": ev.transport.get("to"),
            "day": ev.day,
        }

    # --- Sleep / day-end marker ---
    if ev.kind == "sleep":
        world.last_sleep_location = world.a7do_location
        world.last_sleep_day = ev.day