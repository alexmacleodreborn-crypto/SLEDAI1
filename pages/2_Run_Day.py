import streamlit as st

from world_frame.event_generator import EventGenerator
from a7do_core.event_applier import apply_event
from a7do_core.sleep import sleep_cycle

world = st.session_state.world
a7do = st.session_state.a7do

st.header("▶️ Run Time")

if not world.birthed:
    st.warning("Birth has not occurred yet.")
    st.stop()

generator = EventGenerator()

# ---------------------------
# Run single event
# ---------------------------

if st.button("▶ Run Next Event"):
    event = generator.next_event(world)
    apply_event(a7do, world, event)
    st.success(f"Event applied: {event.label}")

# ---------------------------
# Run full day
# ---------------------------

if st.button("⏩ Run Full Day"):
    events = generator.generate_day(world, n_events=10)
    for ev in events:
        apply_event(a7do, world, ev)
    st.success("Day completed.")

# ---------------------------
# Sleep
# ---------------------------

if st.button("🌙 Sleep"):
    sleep_cycle(a7do)
    world.advance_day()
    st.success("Sleep complete. New day started.")

st.subheader("📅 Time")
st.json({
    "day": world.day,
    "time": world.time,
    "place": world.current_place,
})