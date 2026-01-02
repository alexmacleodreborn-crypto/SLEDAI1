import streamlit as st
from collections import defaultdict

from a7do_core.world_state import WorldState
from a7do_core.events import ExperienceEvent
from a7do_core.event_applier import apply_event
from a7do_core.sleep_replay import run_sleep_replay
from a7do_core.a7do_state import A7DOState


# ─────────────────────────────────────────────
# Streamlit setup
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="A7DO – Cognitive Emergence",
    layout="wide"
)

st.title("🧠 A7DO — Emergent Cognitive Core")
st.caption("Observer-driven experience · No language · No inference")


# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────
if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "preferences" not in st.session_state:
    # tag -> affinity score
    st.session_state.preferences = defaultdict(float)

if "sleep_log" not in st.session_state:
    st.session_state.sleep_log = None


world: WorldState = st.session_state.world


# ─────────────────────────────────────────────
# Helper: derive preference signals
# ─────────────────────────────────────────────
def update_preferences(event: ExperienceEvent):
    """
    Likes / dislikes emerge ONLY from sensory exposure.
    No symbols, no nouns, no semantics.
    """
    for tag, values in event.tags.items():
        if tag in ["sound", "light", "touch", "smell", "taste", "motion"]:
            for v in values:
                st.session_state.preferences[v] += 0.1


# ─────────────────────────────────────────────
# LEFT: Observer Control Panel
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("🎛 Observer Controls")

    if st.button("🌱 Birth Event (Day 0)"):
        birth = ExperienceEvent(
            kind="birth",
            day=0,
            place="hospital",
            duration=1.0,
            tags={
                "sound": ["crying", "voices"],
                "light": ["bright"],
                "touch": ["cold", "wet"],
                "smell": ["clean", "sterile"],
            }
        )
        apply_event(birth, world)
        update_preferences(birth)
        st.success("Birth experience applied")

    st.divider()

    st.subheader("Add Sensory Event")

    place = st.text_input("Place", value="home")
    duration = st.slider("Duration", 0.1, 2.0, 0.5)

    sound = st.text_input("Sound (comma-separated)")
    light = st.text_input("Light")
    touch = st.text_input("Touch")
    smell = st.text_input("Smell")
    motion = st.text_input("Motion")

    if st.button("➕ Apply Event"):
        tags = {}

        if sound:
            tags["sound"] = [s.strip() for s in sound.split(",")]
        if light:
            tags["light"] = [light]
        if touch:
            tags["touch"] = [touch]
        if smell:
            tags["smell"] = [smell]
        if motion:
            tags["motion"] = [motion]

        ev = ExperienceEvent(
            kind="experience",
            day=world.day,
            place=place,
            duration=duration,
            tags=tags
        )

        apply_event(ev, world)
        update_preferences(ev)
        st.success("Event applied")

    st.divider()

    if st.button("🌙 Sleep / Replay"):
        st.session_state.sleep_log = run_sleep_replay(
            world,
            replay_tags=list(world.body_state.keys())
        )
        st.success("Sleep replay complete")


# ─────────────────────────────────────────────
# CENTER: Live A7DO State
# ─────────────────────────────────────────────
st.subheader("🧍 A7DO Current State")

a7do_view = A7DOState(
    current_location=world.location,
    somatic_signals=world.body_state
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Location**")
    st.write(a7do_view.current_location or "—")

    st.markdown("**Day / Time**")
    st.write(f"Day {world.day}, t={world.time:.2f}")

with col2:
    st.markdown("**Somatic Signals**")
    if a7do_view.somatic_signals:
        st.json(a7do_view.somatic_signals)
    else:
        st.write("—")


# ─────────────────────────────────────────────
# RIGHT: Emergent Preferences (NO WORDS)
# ─────────────────────────────────────────────
st.subheader("❤️ Emergent Preferences (Pre-Language)")

if st.session_state.preferences:
    pref_table = sorted(
        st.session_state.preferences.items(),
        key=lambda x: x[1],
        reverse=True
    )
    st.table(
        [{"stimulus": k, "affinity": round(v, 2)} for k, v in pref_table]
    )
else:
    st.write("No preferences yet")


# ─────────────────────────────────────────────
# Sleep Reflection
# ─────────────────────────────────────────────
st.subheader("🌌 Sleep Reflection")

if st.session_state.sleep_log:
    st.markdown("**Replayed Tags**")
    st.write(st.session_state.sleep_log.replayed_tags)

    st.markdown("**Internal Stability**")
    st.json(st.session_state.sleep_log.coherence)
else:
    st.write("No sleep cycle yet")


# ─────────────────────────────────────────────
# Event Timeline
# ─────────────────────────────────────────────
st.subheader("🧾 Event History")

if world.event_history:
    st.write(world.event_history)
else:
    st.write("No events yet")