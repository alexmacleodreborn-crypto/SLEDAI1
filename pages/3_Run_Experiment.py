import streamlit as st
from a7do.caregiver_flow import CaregiverFlow

st.title("▶️ Run Experiment (Control Panel)")

world = st.session_state.get("world")
mind = st.session_state.get("mind")
schedule = st.session_state.get("schedule")

if not world or not mind or not schedule:
    st.warning("System not birthed yet. Open the main page first.")
    st.stop()

st.subheader("Status")
st.json(schedule.status())
st.write("Mind last action:", getattr(mind, "last_action", "—"))

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Wake", disabled=(schedule.state != "sleeping")):
        schedule.authorise_wake()
        st.rerun()

with col2:
    if st.button("🔨 Build Next Day (10 events)", disabled=(schedule.state != "sleeping")):
        flow = CaregiverFlow(world)
        next_day = schedule.day + 1
        evs = flow.build_day(next_day, n_events=10)
        # Start place is where the first event is located (usually home)
        schedule.load(day=next_day, events=evs, start_place=evs[0].place_id, start_room=evs[0].room)
        st.success(f"Built Day {next_day} with {len(evs)} events.")
        st.rerun()

with col3:
    if st.button("▶️ Step", disabled=(schedule.state != "awake")):
        ev = schedule.next_event()
        if ev is None:
            # Day finished: enforce bed + sleep
            schedule.end_day_enforced()
            mind.sleep(day=schedule.day)
        else:
            mind.ingest(ev, day=schedule.day, event_index=schedule.index)
        st.rerun()

st.divider()

st.subheader("Events (Today)")
if schedule.events:
    for i, ev in enumerate(schedule.events, start=1):
        st.write(f"{i}. {ev.summary()}")
else:
    st.info("No events loaded yet. Build the next day to begin.")