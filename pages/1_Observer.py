import streamlit as st
from a7do_core.a7mind import A7DOMind

a7do: A7Mind = st.session_state.a7do

st.header("👁 Observer View")

st.subheader("🧠 Mind State")
st.json({
    "awake": a7do.awake,
    "asleep": a7do.asleep,
})

st.subheader("📓 Internal Log (recent)")
for entry in a7do.internal_log[-10:]:
    st.write(entry)