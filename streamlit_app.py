import streamlit as st
from collections import defaultdict

from a7do_core.world_state import WorldState
from a7do_core.events import ExperienceEvent
from a7do_core.event_applier import apply_event
from a7do_core.a7do_state import A7DOState
from a7do_core.body_local import LocalBody
from a7do_core.action_router import ActionRouter
from a7do_core.gate import SandyGate
from a7do_core.sleep_replay import run_sleep_replay


st.set_page_config(page_title="A7DO – Cognitive Emergence", layout="wide")
st.title("🧠 A7DO — Emergent Cognitive Core (Frozen)")
st.caption("Experience → Preferences → Sleep Replay → Sandy Gate → Permitted Response/Action | Local Body Loops bypass cognition")


# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "world" not in st.session_state:
    st.session_state.world = WorldState()

if "preferences" not in st.session_state:
    st.session_state.preferences = defaultdict(float)  # stimulus -> affinity

if "body" not in st.session_state:
    st.session_state.body = LocalBody()

if "sleep_log" not in st.session_state:
    st.session_state.sleep_log = None

if "last_gate" not in st.session_state:
    st.session_state.last_gate = None

if "last_action" not in st.session_state:
    st.session_state.last_action = None


world: WorldState = st.session_state.world
body: LocalBody = st.session_state.body
router = ActionRouter(body)
gate = SandyGate()


# ─────────────────────────────────────────────
# Preference formation (pre-language)
# ─────────────────────────────────────────────
POS_AFFECT = {"joy", "comfort", "safe", "calm"}
NEG_AFFECT = {"pain", "fear", "cold", "wet", "hungry", "loud", "sharp"}
SENSORY = {"sound", "light", "touch", "smell", "taste", "motion"}


def update_preferences(event: ExperienceEvent):
    valence = 0.0
    affect = (event.tags or {}).get("affect", [])
    for a in affect:
        a = a.strip().lower()
        if a in POS_AFFECT:
            valence += 0.2
        if a in NEG_AFFECT:
            valence -= 0.2
    if valence == 0.0:
        valence = 0.05

    for tag, values in (event.tags or {}).items():
        if tag in SENSORY:
            for v in values:
                stim = v.strip().lower()
                st.session_state.preferences[stim] += valence


def active_stimuli_from_event(event: ExperienceEvent):
    # Create simple bodily stimuli (still pre-language)
    # We keep this minimal and only map a few.
    stim = []
    touch = (event.tags or {}).get("touch", [])
    affect = (event.tags or {}).get("affect", [])

    for t in touch:
        tt = t.strip().lower()
        if tt in {"wet", "cold", "itch", "pain"}:
            stim.append(tt)

    for a in affect:
        aa = a.strip().lower()
        if aa in {"hungry", "pain", "fear"}:
            stim.append(aa)

    return list(dict.fromkeys(stim))


# ─────────────────────────────────────────────
# Sidebar: Controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("🎛 Observer Controls (Frozen Core)")

    caregiver_present = st.checkbox("Caregiver present in scene", value=True)

    st.subheader("Phase 1 — Birth")
    if st.button("🌱 Apply Birth (Day 0)"):
        birth = ExperienceEvent(
            kind="birth",
            day=0,
            place="hospital",
            duration=1.0,
            tags={
                "sound": ["crying", "voices"],
                "light": ["bright"],
                "touch": ["cold", "wet"],
                "smell": ["sterile"],
                "affect": ["fear"],
            }
        )
        apply_event(birth, world)
        update_preferences(birth)

        # Body response permitted
        stimuli = active_stimuli_from_event(birth)
        decision = router.decide(stimuli, caregiver_present)
        if decision.kind != "NONE" and decision.action:
            body.enact(decision.action)
            st.session_state.last_action = decision

        st.success("Birth applied")

    st.divider()
    st.subheader("Phase 2 — Add Experience")

    place = st.text_input("Place", value=(world.location or "home"))
    duration = st.slider("Duration", 0.1, 2.0, 0.5)

    sound = st.text_input("Sound (comma-separated)")
    light = st.text_input("Light")
    touch = st.text_input("Touch")
    smell = st.text_input("Smell")
    taste = st.text_input("Taste")
    motion = st.text_input("Motion")
    affect = st.text_input("Affect (comma-separated: joy/comfort/pain/fear/calm/hungry etc)")

    if st.button("➕ Apply Experience Event"):
        tags = {}
        if sound:
            tags["sound"] = [s.strip() for s in sound.split(",") if s.strip()]
        if light:
            tags["light"] = [light.strip()]
        if touch:
            tags["touch"] = [touch.strip()]
        if smell:
            tags["smell"] = [smell.strip()]
        if taste:
            tags["taste"] = [taste.strip()]
        if motion:
            tags["motion"] = [motion.strip()]
        if affect:
            tags["affect"] = [a.strip() for a in affect.split(",") if a.strip()]

        ev = ExperienceEvent(
            kind="experience",
            day=world.day,
            place=place.strip() or "unknown",
            duration=duration,
            tags=tags
        )

        apply_event(ev, world)
        update_preferences(ev)

        # Body loop (local) can act immediately based on stimuli
        stimuli = active_stimuli_from_event(ev)
        decision = router.decide(stimuli, caregiver_present)
        if decision.kind != "NONE" and decision.action:
            body.enact(decision.action)
            st.session_state.last_action = decision

        st.success("Experience applied")

    st.divider()
    st.subheader("Phase 3 — Sleep / Replay")

    if st.button("🌙 Run Sleep Replay"):
        st.session_state.sleep_log = run_sleep_replay(
            world,
            replay_tags=list(world.body_state.keys()),
            preferences=dict(st.session_state.preferences),
        )
        st.success("Sleep replay complete")

    st.divider()
    st.subheader("Cognitive Gate (demo prompt)")

    demo_prompt = st.text_input("Ask (demo) — will not hallucinate", value="what happened?")
    if st.button("🔍 Evaluate Gate"):
        # Minimal gate inputs:
        # stability from sleep (if present) + signal from body_state sum
        stability = 0.2
        if st.session_state.sleep_log:
            # stable if we have any replayed tags
            stability = 0.7 if st.session_state.sleep_log.replayed_tags else 0.3

        signal = sum(world.body_state.values()) if world.body_state else 0.0
        has_anchor = bool(world.location) and bool(world.event_history)
        resolvable = True  # can always seek help or act in early stage

        st.session_state.last_gate = gate.evaluate(stability, signal, has_anchor, resolvable)
        st.success("Gate evaluated")


# ─────────────────────────────────────────────
# Main panels
# ─────────────────────────────────────────────
a7do_view = A7DOState(current_location=world.location, somatic_signals=world.body_state)

c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.subheader("🧍 A7DO Slice")
    st.write("**Location:**", a7do_view.current_location or "—")
    st.write("**Day / Time:**", f"Day {world.day} · t={world.time:.2f}")
    st.write("**Last Body Action:**", body.last_action or "—")
    if st.session_state.last_action:
        st.caption(f"Action kind: {st.session_state.last_action.kind} · rationale: {', '.join(st.session_state.last_action.rationale)}")

with c2:
    st.subheader("🧠 Somatic Channels (raw)")
    if a7do_view.somatic_signals:
        st.json(a7do_view.somatic_signals)
    else:
        st.write("—")

    st.subheader("🧾 Event History")
    st.write(world.event_history[-30:] if world.event_history else "—")

with c3:
    st.subheader("❤️ Preferences (pre-language)")
    prefs = dict(st.session_state.preferences)
    if prefs:
        comfort = sorted([(k, v) for k, v in prefs.items() if v > 0], key=lambda kv: kv[1], reverse=True)[:10]
        discomfort = sorted([(k, v) for k, v in prefs.items() if v < 0], key=lambda kv: kv[1])[:10]

        st.markdown("**Comfort / Likes**")
        st.table([{"stimulus": k, "affinity": round(v, 2)} for k, v in comfort] or [{"stimulus": "—", "affinity": "—"}])

        st.markdown("**Discomfort / Dislikes**")
        st.table([{"stimulus": k, "affinity": round(v, 2)} for k, v in discomfort] or [{"stimulus": "—", "affinity": "—"}])
    else:
        st.write("No preferences yet.")


st.divider()
st.subheader("🌌 Sleep Reflection")
log = st.session_state.sleep_log
if log:
    a, b, c = st.columns([1, 1, 1])
    with a:
        st.markdown("**Replayed Tags**")
        st.write(log.replayed_tags or "—")
        st.markdown("**Internal Stability**")
        st.json(log.coherence)

    with b:
        st.markdown("**Contrast Summary**")
        st.json(log.contrast_summary)
        st.markdown("**Motor Echoes**")
        st.write(log.motor_echoes or "—")

    with c:
        st.markdown("**Proto-vocalisation (babble)**")
        st.write(log.vocalisations or "—")
        st.markdown("**Self-generated sounds**")
        st.write(log.self_generated_sounds or "—")
else:
    st.write("No sleep cycle yet.")


st.divider()
st.subheader("🔐 Sandy Gate Result (permission layer)")
gr = st.session_state.last_gate
if gr:
    st.write(f"**State:** {gr.state} · **Permitted:** {gr.permitted}")
    st.write(f"Z={gr.z:.2f} · Σ={gr.sigma:.2f}")
    st.write("**Reasons:**", ", ".join(gr.reasons))
else:
    st.write("Gate not evaluated yet.")