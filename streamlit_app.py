import streamlit as st

# ============================================================
# Imports (ONLY new architecture)
# ============================================================

from world_frame.world_state import WorldState
from a7do_core.world_bridge import WorldToA7DOBridge
from a7do_core.a7mind import A7Mind


# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide",
)

st.title("A7DO – Cognitive Emergence")
st.caption("Objective World ⇄ Sensory Bridge ⇄ Embodied Mind")


# ============================================================
# Session State Initialization
# ============================================================

if "world_state" not in st.session_state:
    st.session_state.world_state = WorldState()

if "bridge" not in st.session_state:
    st.session_state.bridge = WorldToA7DOBridge()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7Mind()


world = st.session_state.world_state
bridge = st.session_state.bridge
a7do = st.session_state.a7do


# ============================================================
# Sidebar — World Control
# ============================================================

st.sidebar.header("World Control")

if not world.birthed:
    if st.sidebar.button("🍼 Birth A7DO"):
        world.register_birth()
else:
    st.sidebar.success("A7DO is Birthed")

st.sidebar.divider()

if st.sidebar.button("⏱ Advance Time"):
    world.tick(0.5)

if st.sidebar.button("🚗 Journey Home"):
    world.move_to(
        "Home",
        description="Journey home with parents",
    )

st.sidebar.divider()

if st.sidebar.button("😴 Sleep"):
    a7do.sleep()


# ============================================================
# World → A7DO Bridge
# ============================================================

packets = bridge.pull_new_packets(world)

for pkt in packets:
    a7do.receive_sensory_packet(pkt)


# ============================================================
# Main Display
# ============================================================

left, right = st.columns(2)

# -----------------------------
# World Frame (Objective)
# -----------------------------
with left:
    st.subheader("🌍 World Frame (Objective Reality)")
    st.json(world.snapshot())

    st.subheader("🗺 World Events (Latest)")
    if world.events:
        for ev in world.events[-10:]:
            st.write(
                f"• Day {world.day} @ {ev.time:.2f} — "
                f"{ev.place}: {ev.description}"
            )
    else:
        st.write("No world events yet.")


# -----------------------------
# A7DO Core (Perceived)
# -----------------------------
with right:
    st.subheader("🧠 A7DO Core (Perceived Experience)")
    st.json(a7do.snapshot())

    st.subheader("👶 Recent Sensory Packets")
    if packets:
        for pkt in packets:
            st.write(
                f"• {pkt.place} | "
                f"tags={pkt.tags} | "
                f"sensory={pkt.sensory}"
            )
    else:
        st.write("No new sensory input.")


# ============================================================
# Footer
# ============================================================

st.divider()
st.caption(
    "World Frame = what exists | A7DO Core = what is perceived | "
    "Meaning emerges later through repetition and sleep"
)