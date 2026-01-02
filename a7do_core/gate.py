from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class GateResult:
    permitted: bool
    state: str        # "ANSWER", "KNOWN_UNKNOWN", "ACTION"
    z: float
    sigma: float
    reasons: List[str]


class SandyGate:
    """
    Minimal Sandy’s Law gate for cognition permission.
    - Z = stability/structure
    - Σ = signal/exposure pressure
    This gate does not create meaning; it only permits response/action.
    """

    def __init__(self, z_threshold: float = 0.65, sigma_threshold: float = 0.35):
        self.z_threshold = z_threshold
        self.sigma_threshold = sigma_threshold

    def evaluate(self, stability: float, signal: float, has_anchor: bool, resolvable_by_action: bool) -> GateResult:
        reasons: List[str] = []
        z = float(stability)
        sigma = float(signal)

        if z >= self.z_threshold and sigma >= self.sigma_threshold:
            return GateResult(True, "ANSWER", z, sigma, ["gate_pass"])

        # Not permitted to answer
        if not has_anchor:
            reasons.append("no_anchor")
        if z < self.z_threshold:
            reasons.append("low_stability")
        if sigma < self.sigma_threshold:
            reasons.append("low_signal")

        if resolvable_by_action:
            return GateResult(False, "ACTION", z, sigma, reasons + ["resolvable_by_action"])

        return GateResult(False, "KNOWN_UNKNOWN", z, sigma, reasons + ["not_resolvable"])