# a7do_core/sleep_replay.py
from a7do_core.internal_log import SleepInternalLog
from a7do_core.world_state import WorldState


def run_sleep_replay(world: WorldState, replay_tags: list) -> SleepInternalLog:
    """
    Run sleep replay over selected tags.

    - No new information introduced
    - No world mutation allowed
    """

    world.frozen = True
    log = SleepInternalLog()

    for tag in replay_tags:
        log.replayed_tags.append(tag)

        # Internal correctness = no conflict detected
        # (conflict detection not implemented yet by design)
        log.coherence[tag] = "stable"

    world.frozen = False
    return log