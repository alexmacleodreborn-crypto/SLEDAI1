import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import generate_world, ascii_map, CageBounds

st.set_page_config(page_title="World Cage", layout="wide")
st.title("🧱 World Cage — Spatial & Reality Constraints")

if "world" not in st.session_state:
    st.session_state.world = None

seed = st.number_input("World seed", min_value=1, value=42, step=1)
neigh = st.number_input("Neighbour houses (default 20)", min_value=2, value=20, step=1)

st.subheader("Cage Bounds (Observer-only)")
c1, c2, c3 = st.columns(3)
with c1:
    x_min = st.number_input("x_min", value=-50)
    x_max = st.number_input("x_max", value=50)
with c2:
    y_min = st.number_input("y_min", value=-50)
    y_max = st.number_input("y_max", value=50)
with c3:
    z_min = st.number_input("z_min", value=-2)
    z_max = st.number_input("z_max", value=10)

if st.button("Generate World Cage + Map"):
    w = generate_world(int(seed), neighbour_count=int(neigh))
    # override cage if needed
    w.cage = CageBounds(int(x_min), int(x_max), int(y_min), int(y_max), int(z_min), int(z_max))
    st.session_state.world = w
    st.success("World created. Hospital anchored at (0,0,0).")
    st.rerun()

w = st.session_state.world
if not w:
    st.warning("No world yet. Generate it.")
    st.stop()

st.subheader("Schematic World Listing")
st.code(ascii_map(w))

st.subheader("Anchor Check")
h = w.places["hospital_cwh"]
st.json({
    "hospital_name": h.name,
    "hospital_pos_xyz": h.pos_xyz,
    "hospital_street": h.meta.get("street_name"),
    "cage_bounds": vars(w.cage),
})