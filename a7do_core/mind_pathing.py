from typing import List
from a7do_core.world_state import WorldState


def traverse(anchors: List[str], world: WorldState) -> List[str]:
    """
    Minimal mind-path traversal:
    Returns matching event kinds (no inference).
    """
    path: List[str] = []
    for a in anchors:
        for ev in world.event_history:
            if ev == a:
                path.append(ev)
    return path