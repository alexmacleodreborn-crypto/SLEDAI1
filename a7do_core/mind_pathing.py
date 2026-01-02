# a7do_core/mind_pathing.py
def traverse(anchors: list, world_state):
    """
    Traverse world history using provided anchors.

    Returns a path of matching event kinds.
    No inference or guessing is allowed.
    """

    path = []

    for anchor in anchors:
        for ev in world_state.event_history:
            if anchor == ev:
                path.append(ev)

    return path