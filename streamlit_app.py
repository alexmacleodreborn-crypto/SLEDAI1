import streamlit as st

# ---- Core imports ----
from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle
from a7do_core.event_applier import apply_event
from a7do_core.sleep import sleep_cycle

# ---- World frame imports ----
from world_frame.world_state import WorldState
from world_frame.world_controller import WorldController
from world_frame.event_generator import EventGenerator


# ----------------------------
# Session bootstrap
# ----------------------------
if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()

if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "world_controller" not in st.session_state:
    st.session_state.world_controller = WorldController(st.session_state.world)

if "day_cycle" not in st.session_state:
    st.session_state.day_cycle = DayCycle()

if "event_generator" not in st.session_state:
    st.session_state.event_generator = EventGenerator()

# Aliases (clean + explicit)
a7do = st.session_state.a7do
world = st.session_state.world
world_controller = st.session_state.world_controller
day_cycle = st.session_state.day_cycle
event_generator = st.session_state.event_generator


# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="A7DO – Cognitive Emergence", layout="wide")
st.title("🧠 A7DO – Cognitive Emergence")


# ----------------------------
# Birth control
# ----------------------------
if not a7do.birthed:
    st.subheader("Birth")

    if st.button("🍼 Begin Birth Experience"):
        a7do.birthed = True
        a7do.perceived_world.current_place = "Hospital"
        st.success("A7DO has been born.")
        st.stop()

    st.info("Waiting for birth…")
    st.stop()


# ----------------------------
# Day runner
# ----------------------------
st.subheader(f"Day {a7do.day_index}")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Run Experience Block"):
        # Generate events from the world
        events = event_generator.generate(world, experience="care")

        for ev in events:
            apply_event(a7do, ev)

        st.success(f"Applied {len(events)} experiences.")

with col2:
    if st.button("🌙 Sleep"):
        sleep_cycle(a7do)
        a7do.day_index += 1
        st.success("Sleep complete. New day begins.")


# ----------------------------
# Observer output
# ----------------------------
st.subheader("Observer")

st.markdown("**Current Place**")
st.write(a7do.perceived_world.current_place)

st.markdown("**Perceived Senses**")
st.json(a7do.perceived_world.senses)

st.markdown("**Internal Log**")
st.code("\n".join(a7do.internal_log[-20:]))