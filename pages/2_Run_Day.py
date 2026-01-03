import streamlit as st

world = st.session_state.world
a7do = st.session_state.a7do

st.header("▶️ Run Time")

def load_event_generator():
    """
    Robust loader: tries several known module/class names.
    Update candidates here if your file is named differently.
    """
    candidates = [
        ("world_frame.event_generator", "EventGenerator"),
        ("world_frame.events", "EventGenerator"),
        ("world_frame.generator", "EventGenerator"),
        ("world_frame.event_generator", "Generator"),
        ("world_frame.events", "Generator"),
        ("world_frame.generator", "Generator"),
    ]
    last_err = None
    for mod_name, cls_name in candidates:
        try:
            mod = __import__(mod_name, fromlist=[cls_name])
            cls = getattr(mod, cls_name)
            return cls()
        except Exception as e:
            last_err = e
    raise ImportError(f"Could not load EventGenerator/Generator from world_frame. Last error: {last_err}")

def load_apply_event():
    candidates = [
        ("a7do_core.event_applier", "apply_event"),
        ("a7do_core.event_applier", "apply"),
        ("a7do_core.applier", "apply_event"),
        ("a7do_core.applier", "apply"),
    ]
    last_err = None
    for mod_name, fn_name in candidates:
        try:
            mod = __import__(mod_name, fromlist=[fn_name])
            fn = getattr(mod, fn_name)
            return fn
        except Exception as e:
            last_err = e
    raise ImportError(f"Could not load apply_event from a7do_core. Last error: {last_err}")

def load_sleep_cycle():
    candidates = [
        ("a7do_core.sleep", "sleep_cycle"),
        ("a7do_core.sleep", "sleep"),
        ("a7do_core.sleep", "run_sleep"),
        ("a7do_core.sleep_replay", "sleep_cycle"),
    ]
    last_err = None
    for mod_name, fn_name in candidates:
        try:
            mod = __import__(mod_name, fromlist=[fn_name])
            fn = getattr(mod, fn_name)
            return fn
        except Exception as e:
            last_err = e
    raise ImportError(f"Could not load sleep_cycle from a7do_core. Last error: {last_err}")

# Preconditions
birthed = getattr(world, "birthed", getattr(world, "is_birthed", False))
if not birthed:
    st.warning("Birth has not occurred yet. Go to World Control and trigger birth.")
    st.stop()

# Load functions
try:
    generator = load_event_generator()
    apply_event = load_apply_event()
    sleep_cycle = load_sleep_cycle()
except Exception as e:
    st.error(str(e))
    st.stop()

# Controls
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Run Next Event"):
        ev = generator.next_event(world) if hasattr(generator, "next_event") else generator.next(world)
        apply_event(a7do, world, ev)
        st.success(f"Applied: {getattr(ev, 'label', str(ev))}")

with col2:
    if st.button("⏩ Run Full Day (10 events)"):
        evs = generator.generate_day(world, n_events=10) if hasattr(generator, "generate_day") else generator.generate(world, 10)
        for ev in evs:
            apply_event(a7do, world, ev)
        st.success("Day events applied.")

with col3:
    if st.button("🌙 Sleep (advance day)"):
        sleep_cycle(a7do)
        if hasattr(world, "advance_day"):
            world.advance_day()
        elif hasattr(world, "next_day"):
            world.next_day()
        st.success("Sleep complete → next day")

st.subheader("📅 Time")
st.json({
    "day": getattr(world, "day", getattr(world, "day_index", None)),
    "time": getattr(world, "time", getattr(world, "t", None)),
    "place": getattr(world, "current_place", getattr(world, "place", getattr(world, "location", None))),
})