import streamlit as st
from a7do.world import generate_world, ascii_map, CageBounds

st.title("World Cage (Observer View)")

# Generate or retrieve world
if "world" not in st.session_state:
    st.session_state.world = generate_world()

w = st.session_state.world

# Bounds for observer map
bounds = CageBounds()

st.subheader("World Map (Observer Only)")
st.code(ascii_map(w, bounds))

st.subheader("Places")
for p in w.places.values():
    st.write(f"- {p.label} ({p.kind}) @ {p.pos_xy}")

st.subheader("Bots")
for b in w.bots.values():
    st.write(f"- {b.name} → {b.location} [{b.state}]")