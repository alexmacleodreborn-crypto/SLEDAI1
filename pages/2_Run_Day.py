import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.planner import generate_day

st.set_page_config(page_title="Run Day", layout="wide")
st.title("⏱ Run Day — Schedule → Events → Sleep")

world_map = st.session_state.get("world_map")
profiles = st.session_state.get("profiles")
schedule = st.session_state.get("schedule")
mind = st.session_state.get("mind")

if not world_map or not profiles or not schedule:
    st.info("Create World + Profiles first.")
    st.stop()
if mind is None:
    st.warning("A7DO not born yet. Go to main page and click Birth A7DO.")
    st.stop()

status = schedule.status()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Room", status["room"])
c4.metric("Events Remaining", status["events_remaining"])

st.divider()

cA, cB, cC, cD = st.columns(4)

with cA:
    if st.button("Generate Day Schedule", disabled=not profiles.has_parents()):
        evs = generate_day(world_map, profiles, schedule, day=schedule.day, seed=13)
        schedule.load_day(schedule.day, evs, start_room="bedroom_child")
        st.success(f"Loaded Day {schedule.day} with {len(evs)} events.")
        st.rerun()

with cB:
    if st.button("Wake", disabled=(schedule.state not in ("waiting","complete"))):
        schedule.wake()
        mind.trace.append({"phase": "wake", "day": schedule.day})
        st.rerun()

with cC:
    if st.button("Step 1 Event", disabled=(schedule.state != "awake")):
        ev = schedule.next_event()
        if ev is None:
            schedule.sleep()
            mind.sleep()
            schedule.complete()
        else:
            mind.ingest(ev)
        st.rerun()

with cD:
    if st.button("Run Day", disabled=(schedule.state != "awake")):
        while True:
            ev = schedule.next_event()
            if ev is None:
                schedule.sleep()
                mind.sleep()
                schedule.complete()
                break
            mind.ingest(ev)
        st.rerun()

st.divider()
st.subheader("Queue Preview")
if schedule.events:
    for i, ev in enumerate(schedule.events, 1):
        st.write(f"**{i}.** {ev.building}:{ev.room} | {ev.agent} {ev.action} {ev.obj or ''} → {ev.to_room or ''}")
else:
    st.info("No queue loaded. Generate schedule, then Wake.")

st.divider()
if schedule.state == "complete":
    if st.button("Next Day"):
        schedule.day += 1
        schedule.state = "waiting"
        schedule.events = []
        st.rerun()