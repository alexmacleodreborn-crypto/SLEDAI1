import streamlit as st

from a7do.world import WorldState, BotState
from a7do.caregiver_flow import CaregiverFlow
from a7do.a7do.event_applier import apply_event_to_world

st.title("Run Experiment")

# --- Guards ---
if "world" not in st.session_state:
    st.error("World not initialised. Go to Home.")
    st.stop()

if "current_day" not in st.session_state:
    st.session_state.current_day = 0

if "day_executed" not in st.session_state:
    st.session_state.day_executed = False

flow = CaregiverFlow()

st.write(f"### Day {st.session_state.current_day}")
st.write(f"A7DO location: **{st.session_state.world.a7do_location}**")

# --- Run Day ---
if st.button("Run Day") and not st.session_state.day_executed:
    st.session_state.day_executed = True

    day = st.session_state.current_day
    events = flow.build_day(day, n_events=10)

    for ev in events:
        apply_event_to_world(st.session_state.world, ev)

    st.session_state.last_events = events
    st.success(f"Day {day} executed")


st.markdown("### World Event History")

if not st.session_state.world.event_log:
    st.info("No world events recorded yet.")
else:
    for rec in st.session_state.world.event_log:
        if rec["kind"] == "birth":
            st.success(
                f"🍼 BIRTH — Day {rec['day']} at {rec['place'].upper()}"
            )
        else:
            st.write(
                f"Day {rec['day']} | "
                f"{rec['kind']} @ {rec['place']}"
            )
            
# --- Show events ---
if st.session_state.last_events:
    st.markdown("### Events Today")
    for ev in st.session_state.last_events:
        st.write(
            f"Day {ev.day} | Event {ev.index} | "
            f"{ev.kind.upper()} @ {ev.place}"
        )

# --- Advance ---
if st.session_state.day_executed:
    if st.button("Advance to Next Day"):
        st.session_state.current_day += 1
        st.session_state.day_executed = False
        st.session_state.last_events = []