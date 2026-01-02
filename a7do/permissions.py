# a7do/permissions.py

def is_observer(session_state) -> bool:
    return bool(session_state.get("observer_mode", False))


def lock_ui(session_state) -> bool:
    return not is_observer(session_state)