# streamlit_app.py

import streamlit as st

from a7do_core.a7mind import A7DOMind
from a7do_core.sleep import SleepProcessor
from a7do_core.world_bridge import WorldToA7DOBridge

from world_frame.world_state import WorldState
from world_frame.event_generator import WorldEventGenerator
from world_frame.experience_controller import ExperienceController


# -------------------------------------------------
# Streamlit setup
# -------------------------------------------------

st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide",
)

st.title("🧠 A7DO – Cognitive Emergence")


# -------------------------------------------------
# Session state initialisation
# -------------------------------------------------

if "mind" not in st.session_state:
    st.session_state.mind = A7DOMind()

if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "bridge" not in st.session_state:
    st.session_state.bridge = WorldToA7DOBridge()

if "generator" not in st.session_state:
    st.session_state.generator = WorldEventGenerator()

if "sleep" not in st.session_state:
    st.session_state.sleep = SleepProcessor(st.session_state.mind)

if "experience" not in st.session_state:
    st.session_state.experience = ExperienceController()


mind = st.session_state.mind
world = st.session_state.world
bridge = st.session_state.bridge
generator = st.session_state.generator
sleep = st.session_state.sleep
experience = st.session_state.experience


# -------------------------------------------------
# Helper: run a fixed experience block
# -------------------------------------------------

def run_experience_block(n_steps: int = 6):
    """
    Run a bounded lived experience:
    - generate events
    - translate to sensory packets
    - process perception
    """
    for _ in range(n_steps):
        events = generator.generate(world, experience)
        world.events.extend(events)

        packets = bridge.pull_new_packets(world)
        for pkt in packets:
            mind.process_sensory_packet(pkt)

        world.tick(0.5)


# -------------------------------------------------
# Sidebar – Phase control
# -------------------------------------------------

st.sidebar.header("Life Phases")

st.sidebar.write(f"**Current Phase:** `{experience.phase}`")

# ---- Birth ----
if experience.is_phase("pre_birth"):
    if st.sidebar.button("🍼 Birth A7DO"):
        world.register_birth()
        experience.advance()

# ---- Hospital birth experience ----
elif experience.is_phase("birth"):
    if st.sidebar.button("🏥 Run Hospital Birth Experience"):
        run_experience_block(n_steps=10)
        sleep.sleep_cycle()
        experience.advance()

# ---- Hospital stay ----
elif experience.is_phase("hospital"):
    if st.sidebar.button("🛏 Run Hospital Stay"):
        run_experience_block(n_steps=6)
        sleep.sleep_cycle()
        experience.advance()

# ---- Journey home ----
elif experience.is_phase("journey_home"):
    if st.sidebar.button("🚗 Journey Home"):
        world.move_to("Journey", "Travelling home")
        run_experience_block(n_steps=6)
        world.move_to("Home", "Arrived home")
        experience.advance()

# ---- Home day ----
elif experience.is_phase("home_day"):
    if st.sidebar.button("🏠 Run Home Day"):
        run_experience_block(n_steps=8)
        sleep.sleep_cycle()
        experience.advance()

# ---- Sleep ----
elif experience.is_phase("sleep"):
    if st.sidebar.button("😴 Sleep (End Day)"):
        sleep.sleep_cycle()
        experience.advance()


# -------------------------------------------------
# Main display
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 World State")
    st.json(world.snapshot())

    st.subheader("📜 Recent World Events")
    for ev in world.events[-6:]:
        st.write(
            f"**{ev.place}** @ {round(ev.time,2)} — {ev.description}"
        )

with col2:
    st.subheader("🧠 A7DO Internal State")

    st.metric("Sensory Packets", len(mind.sensory_memory))

    st.subheader("🔁 Familiarity (Prediction Confidence)")
    fam = mind.familiarity.snapshot()
    if fam:
        st.json(fam)
    else:
        st.write("No familiarity formed yet.")

    st.subheader("🛌 Sleep")
    st.write("Sleep consolidates repeated sensory patterns.")