# pages/0_World_Cage.py
import streamlit as st

from a7do.world import WorldState, BotState


st.title("World Cage")

# --- Guard ---
if "world" not in st.session_state:
    st.error("World not initialised yet.")
    st.stop()

world: WorldState = st.session_state.world

# --- World invariants ---
st.markdown("### World State (Observer View)")

col1, col2 = st.columns(2)

with col1:
    st.metric("Current Day", world.current_day)
    st.metric("Current Event Index", world.current_event_index)
    st.metric("A7DO Location", world.a7do_location)
    st.metric("A7DO Posture", world.a7do_posture)

with col2:
    st.metric("Last Sleep Day", world.last_sleep_day)
    st.metric("Last Sleep Location", world.last_sleep_location)

# --- Bots ---
st.markdown("### Other Agents in World")

if not world.bots:
    st.info("No other agents present.")
else:
    for bot in world.bots.values():
        st.write(
            f"- **{bot.name}** "
            f"(location: {bot.location}, "
            f"last seen day {bot.last_seen_day})"
        )

# --- Movement ---
st.markdown("### Recent Movement")

if world.last_movement:
    st.json(world.last_movement)
else:
    st.write("No movement recorded yet.")

# --- Transport ---
st.markdown("### Transport")

if world.last_transport:
    st.json(world.last_transport)
else:
    st.write("No transport events yet.")

st.markdown("---")
st.caption("World Cage is read-only. Reality is updated only via events.")