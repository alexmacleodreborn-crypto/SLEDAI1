import streamlit as st

# --- Core imports ---
from world_frame.world_state import WorldState
from a7do_core.world_bridge import WorldToA7DOBridge
from a7do_core.mind import A7DOMind


# ============================================================
# Streamlit setup
# ============================================================

st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide"
)

st.title("A7DO – Cognitive Emergence")


# ============================================================
# Session State Initialization
# ============================================================

if "world_state" not in st.session_state:
    st.session_state.world_state = WorldState()

if "bridge" not in st.session_state:
    st.session_state.bridge = WorldToA7DOBridge()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOMind()


world = st.session_state.world_state
bridge = st.session_state.bridge
a7do = st.session_state.a7do


# ============================================================
# Control Panel
# ============================================================

st.sidebar.header("World Control")

if not world.birthed:
    if st.sidebar.button("🍼 Birth A7DO"):
        world.register_birth()
else:
    st.sidebar.success("A7DO is birthed")


if st.sidebar.button("⏱ Advance Time"):
    world.tick(0.5)


if st.sidebar.button("🚗 Move to Home"):
    world.move_to("Home", description="Journey home with parents")


# ============================================================
# Bridge: World → A7DO
# ============================================================

packets = bridge.pull_new_packets(world)

for packet in packets:
    # This is where A7DO *feels* the world
    a7do.receive_sensory_packet(packet)


# ============================================================
# Main Display
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 World State (Objective)")
    st.json(world.snapshot())

    st.subheader("🗺 World Events")
    for ev in world.events[-10:]:
        st.write(f"• [{ev.time:.2f}] {ev.place} — {ev.description}")

with col2:
    st.subheader("🧠 A7DO Perceived State")
    st.json(a7do.snapshot())

    st.subheader("👶 Recent Sensory Experience")
    for pkt in packets:
        st.write(
            f"• {pkt.place} | tags={pkt.tags} | sensory={pkt.sensory}"
        )


# ============================================================
# Footer
# ============================================================

st.caption(
    "World Frame = objective reality | A7DO Core = perceived experience"
)