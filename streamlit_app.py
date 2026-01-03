# streamlit_app.py

import streamlit as st

from a7do_core.a7mind import A7DOMind
from a7do_core.sleep import SleepProcessor

from world_frame.world_state import WorldState
from world_frame.event_generator import WorldEventGenerator
from a7do_core.world_bridge import WorldToA7DOBridge


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


mind = st.session_state.mind
world = st.session_state.world
bridge = st.session_state.bridge
generator = st.session_state.generator
sleep = st.session_state.sleep


# -------------------------------------------------
# Controls
# -------------------------------------------------

st.sidebar.header("Controls")

if not world.birthed:
    if st.sidebar.button("🍼 Birth A7DO"):
        world.register_birth()
else:
    if st.sidebar.button("⏱ Advance Time"):
        world.tick(0.5)

    if st.sidebar.button("😴 Sleep"):
        sleep.sleep_cycle()


# -------------------------------------------------
# World processing
# -------------------------------------------------

# Generate world events
events = generator.generate(world)
world.events.extend(events)

# Translate to sensory packets
packets = bridge.pull_new_packets(world)

for pkt in packets:
    mind.process_sensory_packet(pkt)


# -------------------------------------------------
# Main display
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 World State")
    st.json(world.snapshot())

    st.subheader("📜 Recent World Events")
    for ev in world.events[-5:]:
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

    st.subheader("🛌 Sleep Status")
    st.write("Sleep consolidates repeated sensory patterns.")