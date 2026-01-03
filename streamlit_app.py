import streamlit as st

from a7do_core.a7mind import A7Mind
from world_frame.world_state import WorldState

st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide"
)

# --------------------------------------------------
# Session bootstrap
# --------------------------------------------------

if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "a7do" not in st.session_state:
    st.session_state.a7do = A7Mind()

st.title("🧠 A7DO – Cognitive Emergence")
st.caption("Observer-controlled cognitive development environment")

st.success("System initialised. Use the pages on the left.")