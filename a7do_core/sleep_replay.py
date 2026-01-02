from typing import Dict, List

from a7do_core.internal_log import SleepInternalLog
from a7do_core.world_state import WorldState


def _babble_for(stimulus: str) -> str:
    h = sum(ord(c) for c in stimulus) % 6
    return ["ba", "baww", "ga", "mmm", "da", "bbb"][h]


def run_sleep_replay(world: WorldState, replay_tags: List[str], preferences: Dict[str, float]) -> SleepInternalLog:
    """
    Sleep replay:
    - no new world info
    - no mutation
    - validates tags
    - produces contrast (comfort/discomfort)
    - motor echoes
    - proto-vocalisations
    - logs self-generated sounds (babble tokens)
    """
    world.frozen = True
    log = SleepInternalLog()

    # Validate replay tags (placeholder: stable)
    for tag in replay_tags:
        log.replayed_tags.append(tag)
        log.coherence[tag] = "stable"

    # Contrast from preferences
    comfort = []
    discomfort = []
    for stim, score in preferences.items():
        if score >= 0.25:
            comfort.append(stim)
        elif score <= -0.25:
            discomfort.append(stim)

    log.contrast_summary["comfort"] = comfort[:12]
    log.contrast_summary["discomfort"] = discomfort[:12]

    # Motor echoes (pre-language)
    for stim, score in preferences.items():
        if stim in {"rocking", "swaying", "bouncing", "kicking", "crawling"} and score > 0.0:
            log.motor_echoes.append(stim)

    # Proto vocalisation: based on top comfort stimuli (sound-ish tokens)
    top = [k for k, _ in sorted(preferences.items(), key=lambda kv: kv[1], reverse=True)[:8]]
    for s in top[:3]:
        bab = _babble_for(s)
        log.vocalisations.append(bab)

        # Self-generated sound registry (bridge to later speech)
        if bab in {"ba", "da", "ga", "mmm", "bbb", "baww"}:
            if bab not in log.self_generated_sounds:
                log.self_generated_sounds.append(bab)

    world.frozen = False
    return log