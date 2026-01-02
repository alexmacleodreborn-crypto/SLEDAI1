import streamlit as st
from a7do.caregiver_flow import CaregiverFlow
from a7do.newborn_routine import NewbornRoutine

st.title("Run Experiment")

# ---- Session State ----
if "current_day" not in st.session_state:
    st.session_state.current_day = 0

if "day_events" not in st.session_state:
    st.session_state.day_events = None

if "day_executed" not in st.session_state:
    st.session_state.day_executed = False

# ---- Controls ----
overnight = st.checkbox("Overnight in hospital (Day 0)", value=True)
run_newborn = st.checkbox("Use newborn routine (20 days)", value=True)

# ---- Run Day ----
if st.button("Run Day") and not st.session_state.day_executed:
    day = st.session_state.current_day

    if run_newborn:
        routine = NewbornRoutine()
        evs = routine.build_day(day, overnight_in_hospital=overnight)
    else:
        flow = CaregiverFlow(st.session_state.world)
        evs = flow.build_day(day, n_events=10)

    st.session_state.day_events = evs
    st.session_state.day_executed = True

# ---- Display ----
if st.session_state.day_events:
    st.subheader(f"Day {st.session_state.current_day} Events")
    for ev in st.session_state.day_events:
        st.write(
            f"{ev.index:02d} | {ev.place} | "
            f"people={ev.people_present} | "
            f"sounds={ev.sounds} | "
            f"note={ev.note}"
        )

# ---- Advance ----
if st.session_state.day_executed and st.button("Advance to Next Day"):
    st.session_state.current_day += 1
    st.session_state.day_events = None
    st.session_state.day_executed = False