import streamlit as st

from a7do_core.a7do_state import A7DOState
from a7do_core.day_cycle import DayCycle

from world_frame.world_controller import WorldController


st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide"
)

st.title("A7DO – Cognitive Emergence")


# ------------------------------------------------------------------
# Initialise single authoritative instances
# ------------------------------------------------------------------

if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()
    st.session_state.world = WorldController()
    st.session_state.cycle = DayCycle(
        st.session_state.a7do,
        st.session_state.world
    )


a7do = st.session_state.a7do
cycle = st.session_state.cycle


# ------------------------------------------------------------------
# Control Panel
# ------------------------------------------------------------------

st.subheader("Control Panel")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍼 Run Birth", use_container_width=True):
        events = cycle.initialise_if_needed()
        st.success(f"Birth events applied: {len(events)}")

with col2:
    if st.button("🌞 Run Day", use_container_width=True):
        events = cycle.run_day()
        st.success(f"Day events applied: {len(events)}")

with col3:
    if st.button("🌙 Sleep → Next Day", use_container_width=True):
        cycle.sleep()
        cycle.advance_day()
        st.success("Sleep complete, day advanced")


# ------------------------------------------------------------------
# Observer View
# ------------------------------------------------------------------

st.divider()
st.subheader("Observer View")

left, right = st.columns(2)

with left:
    st.markdown("### A7DO State")
    st.json({
        "birthed": a7do.birthed,
        "day_index": a7do.day_index,
        "current_place": a7do.current_place,
    })

with right:
    st.markdown("### Internal Log")
    st.code("\n".join(a7do.internal_log[-20:]), language="text")