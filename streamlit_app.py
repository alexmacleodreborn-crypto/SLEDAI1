import streamlit as st

from a7do_core.world_state import WorldState
from a7do_core.perceived_world_state import PerceivedWorldState
from a7do_core.event_applier import apply_event
from a7do_core.events import ExperienceEvent

from world_frame.places import HOSPITAL, HOME, CAR
from world_frame.transitions import CARRIED, CAR_RIDE
from world_frame.world_controller import WorldController


st.set_page_config(page_title="A7DO – World Frame", layout="wide")

# -----------------------
# Session initialisation
# -----------------------

if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "perceived" not in st.session_state:
    st.session_state.perceived = PerceivedWorldState()

if "controller" not in st.session_state:
    st.session_state.controller = WorldController(st.session_state.world)


world = st.session_state.world
perceived = st.session_state.perceived
controller = st.session_state.controller


# -----------------------
# UI
# -----------------------

st.title("🌍 A7DO – World Frame (Places Only)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Apply Event")

    place = st.selectbox(
        "Place",
        options=[HOSPITAL, CAR, HOME],
        format_func=lambda p: p.name,
    )

    transition = st.selectbox(
        "Transition",
        options=[None, CARRIED, CAR_RIDE],
        format_func=lambda t: "none" if t is None else t.name,
    )

    affect = st.multiselect(
        "Affect tags",
        options=["comfort", "safe", "calm", "joy", "fear", "pain", "cold", "wet", "hungry"],
    )

    duration = st.slider("Duration", 0.1, 5.0, 1.0)

    if st.button("Apply Experience"):
        ev = ExperienceEvent(
            kind="experience",
            place=place,
            tags={"affect": affect},
            duration=duration,
            day=world.day,
        )

        ev = controller.apply_event(ev, place=place, transition=transition)
        apply_event(ev, world, perceived)

with col2:
    st.subheader("🌍 Perceived Places (Subjective)")

    if perceived.familiar_places:
        rows = []
        for name, pm in perceived.familiar_places.items():
            rows.append({
                "place": name,
                "visits": pm.visits,
                "exposure": round(pm.exposure, 2),
                "familiarity": round(pm.familiarity, 2),
                "comfort_bias": round(pm.comfort_bias, 2),
                "last_day": pm.last_day_seen,
            })
        st.table(rows)
    else:
        st.write("No places perceived yet.")

st.divider()
st.write("**Current place:**", perceived.current_place)
st.write("**World day:**", world.day)