import streamlit as st
from world_frame.world_state import WorldState

world: WorldState = st.session_state.world

st.header("🌍 World Control")

# -----------------------------
# World initialisation
# -----------------------------

if not world.initialised:
    if st.button("🌱 Initialise World"):
        world.initialise_world()
        st.success("World initialised.")

else:
    st.info("World already initialised.")

# -----------------------------
# Birth event
# -----------------------------

st.subheader("👶 Birth")

if world.initialised and not world.birthed:
    if st.button("🍼 Trigger Birth (Hospital)"):
        world.trigger_birth()
        st.success("Birth event triggered.")

elif world.birthed:
    st.success("A7DO has been born.")

# -----------------------------
# World status
# -----------------------------

st.subheader("📊 World State")

st.json({
    "initialised": world.initialised,
    "birthed": world.birthed,
    "current_place": world.current_place,
    "day": world.day,
    "time": world.time,
})