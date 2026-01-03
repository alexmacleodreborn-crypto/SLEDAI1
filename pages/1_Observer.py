import streamlit as st
from a7do_core.a7do_state import A7DOState

a7do: A7DOState = st.session_state.a7do

st.header("👁 Observer View")

# -----------------------------
# High-level state
# -----------------------------

st.subheader("🧠 Cognitive State")

st.json({
    "awake": a7do.awake,
    "asleep": a7do.asleep,
    "current_day": a7do.day,
})

# -----------------------------
# Perceived world
# -----------------------------

st.subheader("🌐 Perceived World")

st.json(a7do.perceived_world.snapshot())

# -----------------------------
# Body state
# -----------------------------

st.subheader("🧍 Body State")

st.json(a7do.body.snapshot())

# -----------------------------
# Internal logs
# -----------------------------

st.subheader("📓 Internal Log (recent)")

for entry in a7do.internal_log.tail(10):
    st.write(entry)