from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from .master_core_generation_16_30 import MasterCore30


class MasterCore40(MasterCore30):
    """Generations 31-40: advanced autonomous planning and governance layer."""

    VERSION = "40.0.0"
    MAX_GENERATION = 40
    GENERATIONS = dict(MasterCore30.GENERATIONS, **{
        31: "causal_diagnosis_and_root_cause_analysis",
        32: "predictive_failure_prevention",
        33: "mission_dependency_resolution",
        34: "parallel_safe_workstreams",
        35: "agent_specialization_and_routing",
        36: "evidence_weighted_decision_making",
        37: "policy_simulation_before_action",
        38: "adaptive_test_strategy",
        39: "recovery_budget_and_failure_containment",
        40: "autonomous_operating_system_for_missions",
    })

    ADVANCED_PHASES = list(MasterCore30.ADVANCED_PHASES) + [
        "root_cause", "predict", "dependencies", "parallelize", "route_agents",
        "weigh_evidence", "simulate_policy", "adaptive_test", "contain_failure",
        "operate",
    ]

    def evidence_decision(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Return a conservative decision based on explicit evidence only."""
        trusted = bool(evidence.get("trusted_test_passed"))
        verified = bool(evidence.get("independent_verification_passed"))
        if trusted and verified:
            decision = "continue"
        elif evidence.get("failure"):
            decision = "repair_and_retest"
        else:
            decision = "collect_more_evidence"
        return {"decision": decision, "evidence_required": decision == "collect_more_evidence"}

    def containment_decision(self, repeated_failures: int) -> Dict[str, Any]:
        if repeated_failures >= 3:
            action = "checkpoint_rollback_and_quarantine"
        elif repeated_failures > 0:
            action = "sandbox_repair_with_bounded_retries"
        else:
            action = "normal_execution"
        return {**self.SAFETY_POLICY, "action": action, "timestamp": datetime.now(timezone.utc).isoformat()}

    def status(self):
        result = super().status()
        result.update({
            "version": self.VERSION,
            "max_generation": self.MAX_GENERATION,
            "generation_31_40": {str(k): v for k, v in self.GENERATIONS.items() if k >= 31},
            "advanced_phases": list(self.ADVANCED_PHASES),
            "safety": dict(self.SAFETY_POLICY),
        })
        return result
