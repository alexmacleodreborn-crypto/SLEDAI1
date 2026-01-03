import streamlit as st

world = st.session_state.world

st.header("🌍 World Control")

def _get_bool(obj, *names, default=False):
    for n in names:
        if hasattr(obj, n):
            try:
                return bool(getattr(obj, n))
            except Exception:
                pass
    return default

def _call(obj, *method_names):
    for m in method_names:
        fn = getattr(obj, m, None)
        if callable(fn):
            return fn()
    raise AttributeError(f"No callable found on {type(obj).__name__}: {method_names}")

initialised = _get_bool(world, "initialised", "initialized", "is_initialised", "is_initialized", default=False)
birthed = _get_bool(world, "birthed", "is_birthed", default=False)

# ---------------------------
# Initialise World
# ---------------------------
if not initialised:
    if st.button("🌱 Initialise World"):
        try:
            _call(world, "initialise_world", "initialize_world", "init_world", "build_world")
            st.success("World initialised.")
        except Exception as e:
            st.error(f"Init failed: {e}")
else:
    st.info("World already initialised.")

# Recompute in case init happened
initialised = _get_bool(world, "initialised", "initialized", "is_initialised", "is_initialized", default=False)
birthed = _get_bool(world, "birthed", "is_birthed", default=False)

# ---------------------------
# Trigger Birth
# ---------------------------
st.subheader("👶 Birth")

if initialised and not birthed:
    if st.button("🍼 Trigger Birth (Hospital)"):
        try:
            _call(world, "trigger_birth", "birth", "do_birth", "start_birth")
            st.success("Birth triggered.")
        except Exception as e:
            st.error(f"Birth trigger failed: {e}")
elif birthed:
    st.success("Birth already occurred.")

# ---------------------------
# World Snapshot
# ---------------------------
st.subheader("📊 World State")

st.json({
    "initialised": _get_bool(world, "initialised", "initialized", "is_initialised", "is_initialized", default=None),
    "birthed": _get_bool(world, "birthed", "is_birthed", default=None),
    "current_place": getattr(world, "current_place", getattr(world, "place", getattr(world, "location", None))),
    "day": getattr(world, "day", getattr(world, "day_index", None)),
    "time": getattr(world, "time", getattr(world, "t", None)),
})