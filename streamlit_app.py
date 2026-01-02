import streamlit as st

from a7do.world import WorldState, BotState

st.set_page_config(
    page_title="A7DO",
    layout="wide"
)

st.title("A7DO – Cognitive Experiment")

# --- Initialise world ---
if "world" not in st.session_state:
    world = WorldState()
    world.bots["Mum"] = BotState("Mum", "hospital")
    world.bots["Dad"] = BotState("Dad", "hospital")
    st.session_state.world = world

# --- Initialise experiment state ---
if "current_day" not in st.session_state:
    st.session_state.current_day = 0

if "day_executed" not in st.session_state:
    st.session_state.day_executed = False

if "last_events" not in st.session_state:
    st.session_state.last_events = []

st.markdown("""
### Status
- World initialised
- No experiences yet
- Go to **Run Experiment** to begin Day 0 (birth)
""")

st.write(f"**Current Day:** {st.session_state.current_day}")
st.write(f"**A7DO Location:** {st.session_state.world.a7do_location}")