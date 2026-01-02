import streamlit as st
import sys
import os

# Ensure local imports work
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

st.set_page_config(
    page_title="A7DO",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ─────────────────────────────────────────────
# Core Imports
# ─────────────────────────────────────────────
from a7do.world import WorldMap
from a7do.homeplot import generate_default_home
from a7do.profiles import WorldProfiles
from a7do.schedule import Schedule
from a7do.mind import A7DOMind
from a7do.body import BodyState
from a7do.somatic import SomaticMap

# ─────────────────────────────────────────────
# Streamlit Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="A7DO Cognitive System",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 A7DO — Cognitive Development Environment")

# ─────────────────────────────────────────────
# Session Bootstrap
# ─────────────────────────────────────────────
if "booted" not in st.session_state:
    st.session_state.booted = False

if "world" not in st.session_state:
    st.session_state.world = None

if "profiles" not in st.session_state:
    st.session_state.profiles = None

if "schedule" not in st.session_state:
    st.session_state.schedule = None

if "mind" not in st.session_state:
    st.session_state.mind = None

# ─────────────────────────────────────────────
# Birth / Initialization Panel
# ─────────────────────────────────────────────
if not st.session_state.booted:

    st.subheader("🍼 Birth & World Initialization")

    st.markdown(
        """
        This creates the **only valid reality** A7DO can ever experience.
        Nothing is learned here — only the *world scaffold* is defined.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        seed = st.number_input("World Seed", value=0, step=1)

    with col2:
        confirm = st.checkbox("I understand this defines ground truth")

    if st.button("🟢 Birth A7DO", disabled=not confirm):
        # ─── World
        world = WorldMap(seed=seed)

        # ─── Home
        home = generate_default_home(seed=seed)
        world.places[home.place_id] = home

        # ─── Profiles (Observer knowledge only)
        profiles = WorldProfiles()

        # Parents (required for learning)
        profiles.people["Mum"] = profiles.create_parent(
            name="Mum",
            role="mum",
            age=30,
            hair="brown",
            eyes="green",
        )
        profiles.people["Dad"] = profiles.create_parent(
            name="Dad",
            role="dad",
            age=32,
            hair="dark",
            eyes="blue",
        )

        # ─── Schedule & Body
        schedule = Schedule()
        schedule.body = BodyState()

        # ─── Mind
        mind = A7DOMind(
            world_map=world,
            profiles=profiles,
            schedule=schedule,
            somatic=SomaticMap(),
        )

        # ─── Save to session
        st.session_state.world = world
        st.session_state.profiles = profiles
        st.session_state.schedule = schedule
        st.session_state.mind = mind
        st.session_state.booted = True

        st.success("A7DO has been born. Use the pages to proceed.")
        st.rerun()

    st.stop()

# ─────────────────────────────────────────────
# Main Dashboard (Post-Birth)
# ─────────────────────────────────────────────
world = st.session_state.world
profiles = st.session_state.profiles
schedule = st.session_state.schedule
mind = st.session_state.mind

st.success("A7DO is alive and awaiting experience.")

# ─────────────────────────────────────────────
# Status Overview
# ─────────────────────────────────────────────
st.subheader("Current State")

c1, c2, c3, c4 = st.columns(4)
status = schedule.status()

c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"] or "—")
c4.metric("Cry Level", f"{status['body']['cry']:.2f}")

# ─────────────────────────────────────────────
# Guidance
# ─────────────────────────────────────────────
st.info(
    """
    Use the **Observer** page to:
    • Define the world  
    • Propose future paths  
    • Approve social interactions  

    Use **Run Experiment** to:
    • Load Day 0  
    • Wake A7DO  
    • Step through events  
    • Allow sleep & reflection  
    """
)

# ─────────────────────────────────────────────
# Debug / Transparency (Optional)
# ─────────────────────────────────────────────
with st.expander("🔍 Debug Snapshot (Observer Only)"):
    st.json({
        "world_places": list(world.places.keys()),
        "people": list(profiles.people.keys()),
        "schedule": status,
        "trace_len": len(mind.trace),
        "lexicon_size": len(mind.lexicon),
    })