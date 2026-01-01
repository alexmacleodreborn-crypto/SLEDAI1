import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import ascii_map

st.set_page_config(page_title="Observer", layout="wide")
st.title("👁️ Observer — Learning Formation")

world_map = st.session_state.get("world_map")
profiles = st.session_state.get("profiles")
schedule = st.session_state.get("schedule")
mind = st.session_state.get("mind")

if not world_map or not profiles or not schedule:
    st.info("Create World + Profiles first.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
status = schedule.status()
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Room", status["room"])
c4.metric("Events Remaining", status["events_remaining"])

left, right = st.columns([1, 1])
with left:
    st.subheader("World Map")
    st.code(ascii_map(world_map))

    st.subheader("Body State (signals)")
    st.json(status["body"])

with right:
    st.subheader("Profiles Snapshot")
    st.json(profiles.snapshot())

st.divider()

if mind is None:
    st.warning("A7DO not born yet (mind not initialised). Go to main page → Birth A7DO.")
    st.stop()

st.subheader("Lexicon Exposure (counts)")
st.json(mind.lexicon)

st.subheader("Last Coherence")
st.json(mind.last_coherence or {"note": "none yet"})

st.subheader("Last Sleep Report")
st.json(mind.last_sleep or {"note": "none yet"})

st.divider()
st.subheader("Trace (prompt → structure formation)")

trace = mind.trace[-50:]
if not trace:
    st.info("No trace yet. Run Day events.")
else:
    for t in trace[::-1]:
        phase = t.get("phase")
        if phase == "experience":
            st.markdown("### EXPERIENCE")
            st.code(t.get("prompt","—"))
            st.json(t.get("event", {}))
            st.json({"coherence": t.get("coherence", {})})
        elif phase == "movement":
            st.markdown("### MOVEMENT (inferred)")
            st.write(f"{t.get('from')} → {t.get('to')}")
        elif phase == "blocked":
            st.markdown("### BLOCKED (decoherence protection)")
            st.code(t.get("prompt","—"))
            st.json(t.get("coherence", {}))
        elif phase == "sleep":
            st.markdown("### SLEEP (replay stats)")
            st.json(t.get("report", {}))
        else:
            st.markdown(f"### {phase}")
            st.json(t)