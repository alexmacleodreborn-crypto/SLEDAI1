import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.schedule import Schedule
from a7do.mind import A7DOMind
from a7do.planner import (
    birth_sequence, drive_home_sequence, arrive_home_sequence,
    neighbourhood_meeting_sequence
)

st.set_page_config(page_title="Run Experiment", layout="wide")
st.title("✅ Authorise Experiment Run")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")

if not world:
    st.warning("Create World Cage first.")
    st.stop()
if not profiles or not profiles.has_parents():
    st.warning("Create World Profiles (Mum + Dad) first.")
    st.stop()

if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()
if "mind" not in st.session_state:
    st.session_state.mind = None

schedule = st.session_state.schedule

if st.session_state.mind is None:
    st.session_state.mind = A7DOMind(world_map=world, profiles=profiles, schedule=schedule)
mind = st.session_state.mind

status = schedule.status()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"])
c4.metric("Events Remaining", status["events_remaining"])

st.divider()

st.subheader("Build Day Script")
st.caption("Day 0: Hospital Birth → Drive → Arrive Home → Sleep. Day 1+: Neighbourhood meeting cycles.")

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
    if st.button("Load Day 1 (Neighbourhood Meeting)"):
        doors = list(profiles.neighbour_families.keys())
        evs = neighbourhood_meeting_sequence(world, profiles, schedule, doors=doors)
        schedule.load(1, evs, start_place="house_a7do", start_room="living_room")
        st.success(f"Loaded Day 1 with {len(evs)} events.")
        st.rerun()

with colC:
    if st.button("Authorise Wake"):
        schedule.authorise_wake()
        mind.trace.append({"phase": "wake", "day": schedule.day, "place_id": schedule.spatial.place_id})
        st.rerun()

st.divider()

cX, cY, cZ = st.columns(3)
with cX:
    if st.button("Step 1 Event", disabled=(schedule.state != "awake")):
        ev = schedule.next_event()
        if ev is None:
            schedule.sleep()
            mind.sleep()
            schedule.complete()
        else:
            mind.ingest(ev)
        st.rerun()

with cY:
    if st.button("Run All Events", disabled=(schedule.state != "awake")):
        while True:
            ev = schedule.next_event()
            if ev is None:
                schedule.sleep()
                mind.sleep()
                schedule.complete()
                break
            mind.ingest(ev)
        st.rerun()

with cZ:
    if st.button("Advance to Day 1", disabled=(schedule.state != "complete")):
        schedule.day = 1
        schedule.state = "waiting"
        schedule.queue = []
        st.rerun()

st.divider()
st.subheader("Queue Preview")
if schedule.queue:
    for i, ev in enumerate(schedule.queue[:20], 1):
        st.write(f"**{i}.** {ev.place_id}:{ev.room} | {ev.agent} {ev.action} {ev.obj or ''} → {ev.to_place_id or ''}")
else:
    st.info("No queue loaded. Load a day script, then Authorise Wake.")