from dataclasses import dataclass
from typing import List, Optional

from a7do_core.body_local import LocalBody


@dataclass
class ActionDecision:
    kind: str                 # "BODY_REFLEX" | "SEEK_HELP" | "NONE"
    action: Optional[str]     # action label if any
    rationale: List[str]


class ActionRouter:
    """
    If cognition cannot answer, actions may be permitted:
    - Body reflex (local)
    - Seek help (cry, call caregiver)
    """

    def __init__(self, body: LocalBody):
        self.body = body

    def decide(self, active_stimuli: List[str], caregiver_present: bool) -> ActionDecision:
        # Try local reflex first
        reflex = self.body.choose_action(active_stimuli)
        if reflex:
            return ActionDecision("BODY_REFLEX", reflex, ["local_reflex"])

        # If discomfort and no reflex, seek help by crying (pre-language)
        if any(s in {"wet", "cold", "pain", "hungry", "itch"} for s in active_stimuli):
            if caregiver_present:
                return ActionDecision("SEEK_HELP", "cry", ["seek_help", "caregiver_present"])
            return ActionDecision("SEEK_HELP", "cry", ["seek_help", "caregiver_absent"])

        return ActionDecision("NONE", None, ["no_action_needed"])