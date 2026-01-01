import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import ascii_map
from a7do.future_paths import FuturePathRegistry
from a7do.bot import propose_paths

st.title("👁️ Observer — World / Trace / Paths")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")
schedule = st.session_state.get("schedule")
mind = st.session_state.get("mind")

if not world or not profiles or not schedule or not mind:
    st.warning("Need World + Profiles + Mind (create via Run Experiment).")
    st.stop()

if "future_paths" not in st.session_state:
    st.session_state.future_paths = FuturePathRegistry()
registry = st.session_state.future_paths

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

    st.subheader("Somatic Snapshot (scaffold)")
    st.json(mind.somatic.snapshot())

with right:
    st.subheader("Profiles Snapshot")
    st.json(profiles.snapshot())

st.divider()

st.subheader("Future Paths Registry (Bots propose options; Observer approves)")

colA, colB = st.columns(2)
with colA:
    if st.button("CurriculumBot: Propose Paths"):
        propose_paths("CurriculumBot", registry, world, profiles, mind)
        st.success("Proposals added (options only).")
        st.rerun()

    st.write("### Proposed")
    for p in registry.list(status="proposed")[:20]:
        st.write(f"**{p.path_id}** | {p.type} | priority={p.priority} novelty={p.novelty_cost}")
        st.json({"proposal": p.proposal, "unlock": p.unlock, "notes": p.notes})
        if st.button(f"Approve {p.path_id}", key=f"ap_{p.path_id}"):
            registry.approve(p.path_id)
            st.rerun()

with colB:
    st.write("### Approved")
    approved = registry.list(status="approved")
    if not approved:
        st.info("No approved paths. Approve from the left.")
    for p in approved[:20]:
        st.write(f"**{p.path_id}** | {p.type}")
        st.json({"proposal": p.proposal, "unlock": p.unlock, "notes": p.notes})

st.divider()

st.subheader("Trace (latest first)")
trace = mind.trace[-60:]
if not trace:
    st.info("No events yet.")
else:
    for t in trace[::-1]:
        st.markdown(f"### {t.get('phase','—').upper()}")
        st.json(t)

st.subheader("Lexicon Exposure")
st.json(mind.lexicon)

st.subheader("Last Sleep Report")
st.json(mind.last_sleep or {"note": "none yet"})