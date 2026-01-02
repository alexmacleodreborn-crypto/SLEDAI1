import streamlit as st

from a7do.world import WorldState, BotState
from a7do.caregiver_flow import CaregiverFlow
from a7do.a7do.event_applier import apply_event_to_world


# Initialise session
if "world" not in st.session_state:
    world = WorldState()
    world.bots["Mum"] = BotState("Mum", "hospital")
    world.bots["Dad"] = BotState("Dad", "hospital")
    st.session_state.world = world

if "current_day" not in st.session_state:
    st.session_state.current_day = 0

if "day_executed" not in st.session_state:
    st.session_state.day_executed = False


flow = CaregiverFlow()

st.title("Run Experiment")

st.write(f"Day: {st.session_state.current_day}")
st.write(f"A7DO location: {st.session_state.world.a7do_location}")

# Run day once
if st.button("Run Day") and not st.session_state.day_executed:
    st.session_state.day_executed = True

    day = st.session_state.current_day
    events = flow.build_day(day, n_events=10)

    for ev in events:
        apply_event_to_world(st.session_state.world, ev)

    st.session_state.last_events = events
    st.success("Day executed")

# Advance
if st.session_state.day_executed:
    if st.button("Advance to Next Day"):
        st.session_state.current_day += 1
        st.session_state.day_executed = False