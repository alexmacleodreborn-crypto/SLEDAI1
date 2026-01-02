import streamlit as st
import sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

st.set_page_config(page_title="A7DO", page_icon="🧠", layout="wide")

from a7do.world import generate_world
from a7do.mind import A7DOMind
from a7do.schedule import Schedule

st.title("🧠 A7DO — Developmental Simulation")

# Auto-create once
if "world" not in st.session_state:
    st.session_state.world = generate_world(seed=7)

if "mind" not in st.session_state:
    st.session_state.mind = A7DOMind()

if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()
    # Start at day 0 sleeping in hospital by default
    st.session_state.schedule.load(
        day=0,
        events=[],
        start_place="hospital",
        start_room="ward",
    )

world = st.session_state.world
mind = st.session_state.mind
schedule = st.session_state.schedule

st.subheader("System Snapshot")
st.json({
    "world_places": len(world.places),
    "world_bots": len(world.bots),
    "schedule": schedule.status(),
    "mind": mind.summary(),
})

st.info("Use **Run Experiment** to build days and step events. Use **Observer** to inspect learning.")