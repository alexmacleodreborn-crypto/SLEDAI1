import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

import streamlit as st
from a7do.profiles import WorldProfiles, PersonProfile, AnimalProfile, ObjectProfile

st.set_page_config(page_title="World Profile", layout="wide")
st.title("👪 World Profile — Families, Pets, Objects")

if "profiles" not in st.session_state:
    st.session_state.profiles = WorldProfiles()

profiles = st.session_state.profiles

st.subheader("Core Family (A7DO origin)")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Create Mum/Dad/Sister (defaults)"):
        profiles.people["Mum"] = PersonProfile("Mum", "mum", 31, "brown", "green", ["warm voice", "soft smile"])
        profiles.people["Dad"] = PersonProfile("Dad", "dad", 34, "black", "brown", ["calm voice", "short beard"])
        profiles.people["Sister"] = PersonProfile("Sister", "sister", 6, "brown", "blue", ["small voice"])
        st.success("Core family created.")
        st.rerun()

with c2:
    if st.button("Create Pet Xena (dog)"):
        profiles.animals["Xena"] = AnimalProfile("Xena", "dog", "excited", ["bark"])
        profiles.assign_pet("Xena", "Mum")
        st.success("Xena created and linked to Mum as pet.")
        st.rerun()

with c3:
    if st.button("Create Basic Objects"):
        profiles.objects["ball"] = ObjectProfile("ball", "toy", colour="red", shape="round", affordances=["roll", "throw", "catch"])
        profiles.objects["pram"] = ObjectProfile("pram", "furniture", colour="grey", shape=None, affordances=["push"])
        st.success("Objects created.")
        st.rerun()

st.divider()

st.subheader("Neighbourhood Families (20 houses)")
st.caption("Rules: odd door→car, even door→dog, plus 3 special families (single mum, single dad, blended).")

doors = [str(i) for i in range(2, 22)]  # 20 neighbours door numbers (2..21)
seed = st.number_input("Neighbour seed", min_value=1, value=99, step=1)

if st.button("Generate Neighbour Families"):
    profiles.generate_neighbours(int(seed), doors)
    st.success(f"Generated neighbour families for doors {doors[0]}..{doors[-1]}.")
    st.rerun()

st.divider()
st.subheader("Current Profiles Snapshot")
st.json(profiles.snapshot())