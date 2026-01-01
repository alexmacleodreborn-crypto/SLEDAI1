import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.world import generate_neighbourhood, ascii_map
from a7do.profiles import PersonProfile, AnimalProfile, ObjectProfile

st.set_page_config(page_title="World Profile", layout="wide")
st.title("🌍 World Profile (Observer-only)")

if "world_map" not in st.session_state:
    st.session_state.world_map = None
if "profiles" not in st.session_state:
    from a7do.profiles import WorldProfiles
    st.session_state.profiles = WorldProfiles()
if "schedule" not in st.session_state:
    from a7do.schedule import Schedule
    st.session_state.schedule = Schedule()

world_map = st.session_state.world_map
profiles = st.session_state.profiles
schedule = st.session_state.schedule

seed = st.number_input("World seed", min_value=1, value=int(schedule.world_seed), step=1)
schedule.world_seed = int(seed)

c1, c2 = st.columns(2)
with c1:
    if st.button("Generate / Regenerate World"):
        st.session_state.world_map = generate_neighbourhood(int(seed))
        schedule.world_ready = True
        st.success("World generated.")
        st.rerun()

with c2:
    if world_map:
        st.code(ascii_map(world_map))
        st.caption("A=A7DO house, N=neighbour, P=park, S=street")
    else:
        st.info("No world yet.")

st.divider()
st.subheader("Family Profiles (must include Mum + Dad)")

with st.form("add_person"):
    name = st.text_input("Name")
    role = st.selectbox("Role", ["mum", "dad", "neighbour"])
    age = st.number_input("Age", min_value=0, value=30)
    hair = st.text_input("Hair colour")
    eyes = st.text_input("Eye colour")
    features = st.text_input("Features (comma-separated)")
    if st.form_submit_button("Add / Update Person") and name:
        profiles.people[name] = PersonProfile(
            name=name, role=role, age=int(age), hair=hair, eyes=eyes,
            features=[f.strip() for f in features.split(",") if f.strip()]
        )
        st.rerun()

st.subheader("Animals")
with st.form("add_animal"):
    name = st.text_input("Animal name")
    species = st.text_input("Species")
    temperament = st.text_input("Temperament", value="calm")
    sounds = st.text_input("Sounds (comma)", value="bark" if species.lower()=="dog" else "")
    if st.form_submit_button("Add / Update Animal") and name and species:
        profiles.animals[name] = AnimalProfile(
            name=name, species=species, temperament=temperament,
            sounds=[s.strip() for s in sounds.split(",") if s.strip()]
        )
        st.rerun()

st.subheader("Objects")
with st.form("add_object"):
    name = st.text_input("Object name")
    category = st.selectbox("Category", ["toy", "tool", "container", "furniture", "other"])
    colour = st.text_input("Colour")
    shape = st.text_input("Shape")
    aff = st.text_input("Affordances (comma)", value="roll, throw, catch" if name.lower()=="ball" else "")
    if st.form_submit_button("Add / Update Object") and name:
        profiles.objects[name] = ObjectProfile(
            name=name, category=category, colour=colour or None, shape=shape or None,
            affordances=[a.strip() for a in aff.split(",") if a.strip()]
        )
        st.rerun()

st.divider()
st.subheader("Snapshot")
st.json(profiles.snapshot())