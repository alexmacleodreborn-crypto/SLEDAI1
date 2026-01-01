import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st

from a7do.schedule import Schedule
from a7do.mind import A7DOMind
from a7do.planner import birth_sequence, drive_home_sequence, arrive_home_sequence
from a7do.future_paths import FuturePathRegistry
from a7do.events import ExperienceEvent
from a7do.profiles import ObjectProfile

st.title("▶️ Run Experiment — Authorised Events Only")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")

if not world:
    st.warning("Create the World Cage first.")
    st.stop()

if not profiles or not profiles.has_parents():
    st.warning("Create Mum and Dad in World Profile first.")
    st.stop()

# ─────────────────────────────────────────────
# Initialise Core Components
# ─────────────────────────────────────────────
if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()
schedule = st.session_state.schedule

if "mind" not in st.session_state:
    st.session_state.mind = A7DOMind(world_map=world, profiles=profiles, schedule=schedule)
mind = st.session_state.mind

if "future_paths" not in st.session_state:
    st.session_state.future_paths = FuturePathRegistry()
registry = st.session_state.future_paths

status = schedule.status()

# ─────────────────────────────────────────────
# Status Bar
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"])
c4.metric("Events Remaining", status["events_remaining"])

# ─────────────────────────────────────────────
# Day Controls
# ─────────────────────────────────────────────
st.divider()
colA, colB, colC = st.columns(3)

with colA:
    if st.button("Load Day 0 (Birth → Drive → Home)"):
        evs = []
        evs += birth_sequence(world, schedule)
        evs += drive_home_sequence(world, schedule)
        evs += arrive_home_sequence(world, schedule)
        schedule.load(0, evs, start_place="hospital_cwh", start_room="delivery_room")
        st.success(f"Loaded Day 0 with {len(evs)} events.")
        st.rerun()

with colB:
    if st.button("Authorise Wake"):
        schedule.authorise_wake()
        mind.trace.append({"phase": "wake", "day": schedule.day})
        st.rerun()

with colC:
    if st.button("Step Next Event", disabled=(schedule.state != "awake")):
        ev = schedule.next_event()
        if ev is None:
            schedule.sleep()
            mind.sleep()
            schedule.complete()
        else:
            mind.ingest(ev)
        st.rerun()

# ─────────────────────────────────────────────
# Build Next Day from Approved Paths
# ─────────────────────────────────────────────
st.divider()
st.subheader("Build Next Day from Approved Paths")

if st.button("Build Day from Approved Paths"):
    approved = registry.list(status="approved")
    if not approved:
        st.warning("No approved paths.")
    else:
        evs = []
        start_place, start_room = "house_a7do", "living_room"

        for p in approved[:12]:
            # Object exposure
            if p.type == "object":
                name = p.proposal.get("name", "object")
                if name not in profiles.objects:
                    profiles.objects[name] = ObjectProfile(
                        name=name,
                        category=p.proposal.get("category", "toy"),
                        colour=p.proposal.get("colour"),
                        shape=p.proposal.get("shape"),
                        affordances=p.proposal.get("affordances", []),
                    )

                evs.append(ExperienceEvent(
                    place_id=start_place,
                    room=start_room,
                    agent="Dad",
                    action="showed",
                    obj=name,
                    emphasis=[name.upper()],
                    sound={"pattern": "gentle voice"},
                    touch={"pattern": "held near hands"},
                    presence=["Dad", "Mum"],
                    body=schedule.body.snapshot(),
                ))
                registry.mark_scheduled(p.path_id)

            # Neighbour visit routine
            elif p.type == "routine" and p.proposal.get("name") == "neighbour_visit":
                visitor = p.proposal["visitor"]

                evs.extend([
                    ExperienceEvent(
                        place_id="house_a7do",
                        room="hall",
                        agent="Street",
                        action="knocked",
                        sound={"pattern": "knock knock"},
                        presence=["Mum", "Dad"],
                        body=schedule.body.snapshot(),
                    ),
                    ExperienceEvent(
                        place_id="house_a7do",
                        room="hall",
                        agent=visitor,
                        action="said",
                        obj="hello",
                        sound={"pattern": "friendly voice"},
                        presence=[visitor, "Mum", "Dad"],
                        body=schedule.body.snapshot(),
                        transaction={"target": "A7DO", "outcome": "calm"},
                    ),
                    ExperienceEvent(
                        place_id="house_a7do",
                        room="hall",
                        agent=visitor,
                        action="left",
                        body=schedule.body.snapshot(),
                    ),
                ])
                registry.mark_scheduled(p.path_id)

            # Park routine
            elif p.type == "routine" and p.proposal.get("name") == "short_walk_to_park":
                evs.append(ExperienceEvent(
                    place_id="house_a7do",
                    room="hall",
                    agent="Mum",
                    action="carried",
                    obj="you",
                    motor={"type": "carried", "intensity": "steady"},
                    to_place_id="park_01",
                    pos_xyz=world.places["park_01"].pos_xyz,
                    sound={"pattern": "outside air"},
                    smell={"pattern": "grass"},
                    presence=["Mum", "Dad"],
                    body=schedule.body.snapshot(),
                ))
                registry.mark_scheduled(p.path_id)

        schedule.load(schedule.day + 1, evs, start_place=start_place, start_room=start_room)
        st.success(f"Built Day {schedule.day} with {len(evs)} events.")
        st.rerun()

# ─────────────────────────────────────────────
# Queue Preview
# ─────────────────────────────────────────────
st.divider()
st.subheader("Event Queue Preview")

if not schedule.queue:
    st.info("No events queued.")
else:
    for i, ev in enumerate(schedule.queue, 1):
        st.write(
            f"{i}. {ev.place_id}:{ev.room} | {ev.agent} {ev.action} {ev.obj or ''}"
        )