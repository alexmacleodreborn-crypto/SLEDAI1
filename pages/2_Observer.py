import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import ascii_map
from a7do.future_paths import FuturePathRegistry
from a7do.bot import propose_paths
from a7do.neighbour_bot import propose_neighbour_visit

st.title("👁️ Observer — World, Trace & Future Paths")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")
schedule = st.session_state.get("schedule")
mind = st.session_state.get("mind")

if not world or not profiles or not schedule or not mind:
    st.warning("World, Profiles, Schedule, and Mind must be initialised.")
    st.stop()

# Registry lives ONLY observer-side
if "future_paths" not in st.session_state:
    st.session_state.future_paths = FuturePathRegistry()
registry = st.session_state.future_paths

status = schedule.status()

# ─────────────────────────────────────────────
# Status Bar
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"])
c4.metric("Events Remaining", status["events_remaining"])

# ─────────────────────────────────────────────
# World & Body Views
# ─────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.subheader("World Cage (Observer Reality)")
    st.code(ascii_map(world))

    st.subheader("A7DO Body State")
    st.json(status["body"])

    st.subheader("Somatic Scaffold (Touch/Pain)")
    st.json(mind.somatic.snapshot())

with right:
    st.subheader("World Profiles Snapshot")
    st.json(profiles.snapshot())

# ─────────────────────────────────────────────
# Future Path Registry
# ─────────────────────────────────────────────
st.divider()
st.subheader("Future Paths (Bots → Observer → Schedule)")

colA, colB = st.columns(2)

with colA:
    st.write("### Proposal Generators")

    if st.button("CurriculumBot: Propose Learning Paths"):
        propose_paths("CurriculumBot", registry, world, profiles, mind)
        st.success("Curriculum paths proposed.")
        st.rerun()

    if st.button("NeighbourBot: Propose Neighbour Visit"):
        propose_neighbour_visit(registry, world, profiles, mind)
        st.success("Neighbour visit proposed (if safe).")
        st.rerun()

    st.write("### Proposed Paths")
    for p in registry.list(status="proposed"):
        st.markdown(f"**{p.path_id}** · `{p.type}` · priority={p.priority}")
        st.json({
            "proposal": p.proposal,
            "unlock": p.unlock,
            "novelty_cost": p.novelty_cost,
            "notes": p.notes,
        })
        if st.button(f"Approve {p.path_id}", key=f"approve_{p.path_id}"):
            registry.approve(p.path_id)
            st.rerun()

with colB:
    st.write("### Approved (Ready for Scheduling)")
    approved = registry.list(status="approved")
    if not approved:
        st.info("No approved paths yet.")
    for p in approved:
        st.markdown(f"**{p.path_id}** · `{p.type}`")
        st.json(p.proposal)

# ─────────────────────────────────────────────
# Trace & Memory
# ─────────────────────────────────────────────
st.divider()
st.subheader("A7DO Trace (Latest First)")

if not mind.trace:
    st.info("No experiences yet.")
else:
    for t in mind.trace[::-1][:40]:
        st.markdown(f"### {t.get('phase','—').upper()}")
        st.json(t)

st.subheader("Lexicon Exposure")
st.json(mind.lexicon)

st.subheader("Last Sleep Replay")
st.json(mind.last_sleep or {"note": "No sleep yet"})