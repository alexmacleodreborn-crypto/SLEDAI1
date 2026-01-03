import streamlit as st

# DO NOT type-annotate with A7Mind / A7DOState etc.
a7do = st.session_state.a7do
world = st.session_state.world

st.header("👁 Observer View")

st.subheader("World (objective)")
st.json({
    "place": getattr(world, "current_place", getattr(world, "place", getattr(world, "location", None))),
    "day": getattr(world, "day", getattr(world, "day_index", None)),
    "time": getattr(world, "time", getattr(world, "t", None)),
    "birthed": getattr(world, "birthed", getattr(world, "is_birthed", None)),
})

st.subheader("A7DO (internal)")

st.json({
    "awake": getattr(a7do, "awake", None),
    "asleep": getattr(a7do, "asleep", None),
    "stage": getattr(a7do, "stage", getattr(a7do, "development_stage", None)),
})

# Perceived world
st.subheader("Perceived World")
pw = getattr(a7do, "perceived_world_state", None) or getattr(a7do, "perceived_world", None)
if pw is None:
    st.info("No perceived world module found on mind yet.")
else:
    snap = pw.snapshot() if hasattr(pw, "snapshot") else getattr(pw, "__dict__", {})
    st.json(snap)

# Body / somatic
st.subheader("Body / Somatic")
body = getattr(a7do, "body", None) or getattr(a7do, "body_local", None) or getattr(a7do, "somatic", None)
if body is None:
    st.info("No body module found on mind yet.")
else:
    snap = body.snapshot() if hasattr(body, "snapshot") else getattr(body, "__dict__", {})
    st.json(snap)

# Internal log
st.subheader("Internal Log (recent)")
log = getattr(a7do, "internal_log", None) or getattr(a7do, "log", None)
if log is None:
    st.info("No internal log found on mind yet.")
else:
    if isinstance(log, list):
        recent = log[-20:]
    elif hasattr(log, "tail"):
        recent = log.tail(20)
    else:
        recent = [str(log)]
    for entry in recent:
        st.write(entry)