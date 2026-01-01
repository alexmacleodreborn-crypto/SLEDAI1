import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from a7do.world import generate_neighbourhood, ascii_map
from a7do.profiles import WorldProfiles, PersonProfile, AnimalProfile, ObjectProfile
from a7do.schedule import Schedule
from a7do.mind import A7DOMind
from a7do.planner import generate_day, make_parent_knowledge

st.set_page_config(page_title="A7DO Clean v1", layout="wide")

# --- session init
if "world_map" not in st.session_state:
    st.session_state.world_map = None
if "profiles" not in st.session_state:
    st.session_state.profiles = WorldProfiles()
if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()
if "mind" not in st.session_state:
    st.session_state.mind = None

world_map = st.session_state.world_map
profiles = st.session_state.profiles
schedule = st.session_state.schedule

st.title("🧠 A7DO — Clean App v1")

# Birth gate
left, right = st.columns([1, 1])
with left:
    st.subheader("Central Status")
    if world_map is None:
        st.warning("WAITING — BIRTHING (World not generated)")
    elif not profiles.has_parents():
        st.warning("WAITING — BIRTHING (Mum + Dad missing)")
    else:
        st.success("READY — World + Parents present")

with right:
    st.subheader("Quick World View")
    if world_map:
        st.code(ascii_map(world_map))
        st.caption("Legend: A=A7DO house, N=neighbour, P=park, S=street")

st.divider()

st.subheader("Shortcuts")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Generate World (seed=42)"):
        schedule.world_seed = 42
        st.session_state.world_map = generate_neighbourhood(42)
        schedule.world_ready = True
        st.success("World generated.")
        st.rerun()

with c2:
    if st.button("Auto-create Family + Defaults"):
        # parents
        profiles.people["Mum"] = PersonProfile(name="Mum", role="mum", age=31, hair="brown", eyes="green",
                                              features=["soft smile", "warm voice"])
        profiles.people["Dad"] = PersonProfile(name="Dad", role="dad", age=34, hair="black", eyes="brown",
                                              features=["short beard", "calm voice"])
        # defaults
        profiles.objects["ball"] = ObjectProfile(name="ball", category="toy", colour="red", shape="round",
                                                 affordances=["roll", "throw", "catch"])
        profiles.animals["Xena"] = AnimalProfile(name="Xena", species="dog", temperament="excited", sounds=["bark"])
        # parent knowledge (background)
        profiles.parent_knowledge["Mum"] = make_parent_knowledge(schedule.world_seed + 1)
        profiles.parent_knowledge["Dad"] = make_parent_knowledge(schedule.world_seed + 2)

        st.success("Family + defaults created.")
        st.rerun()

with c3:
    if st.button("Birth A7DO (init mind)", disabled=(st.session_state.world_map is None)):
        if st.session_state.mind is None:
            st.session_state.mind = A7DOMind(schedule=schedule, world_map=st.session_state.world_map, profiles=profiles)
        st.success("A7DO born (algorithms loaded; knowledge empty).")
        st.rerun()

st.info("Use the left Pages menu: World Profile → Observer → Run Day.")