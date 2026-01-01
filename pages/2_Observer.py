import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import ascii_map

st.set_page_config(page_title="Observer", layout="wide")
st.title("👁️ Observer — World / Trace / Learning")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")
schedule = st.session_state.get("schedule")
mind = st.session_state.get("mind")

if not world or not profiles or not schedule or not mind:
    st.warning("Need World Cage + Profiles + Mind (Run Experiment page creates mind).")
    st.stop()

status = schedule.status()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"])
c4.metric("Events Remaining", status["events_remaining"])

left, right = st.columns([1, 1])
with left:
    st.subheader("World Schematic")
    st.code(ascii_map(world))

    st.subheader("Body State")
    st.json(status["body"])

    st.subheader("Last Action")
    st.write(mind.last_action or "—")

with right:
    st.subheader("Profiles Snapshot")
    st.json(profiles.snapshot())

st.divider()

cA, cB, cC = st.columns(3)
with cA:
    st.subheader("Lexicon Exposure")
    st.json(mind.lexicon)

with cB:
    st.subheader("Last Coherence")
    st.json(mind.last_coherence or {"note": "none yet"})

with cC:
    st.subheader("Last Sleep Report")
    st.json(mind.last_sleep or {"note": "none yet"})

st.divider()
st.subheader("Trace (latest first)")
trace = mind.trace[-60:]
if not trace:
    st.info("No events yet. Run experiment.")
else:
    for t in trace[::-1]:
        phase = t.get("phase", "—")
        st.markdown(f"### {phase.upper()}")
        if phase == "experience":
            st.code(t.get("prompt", "—"))
            st.json(t.get("event", {}))
            st.json({"coherence": t.get("coherence", {})})
        else:
            st.json(t)