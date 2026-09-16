from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from .master_core import MasterCore


class MasterCore30(MasterCore):
    """Master Agent extension covering generations 16 through 30."""

    VERSION = "30.0.0"
    MAX_GENERATION = 30
    GENERATIONS = MasterCore.GENERATIONS.copy()
    GENERATIONS.update({
        16: "self_verification_and_quality_control",
        17: "failure_pattern_learning",
        18: "adaptive_recovery",
        19: "mission_deduplication_and_prioritization",
        20: "resource_and_cost_awareness",
        21: "security_posture_and_policy_validation",
        22: "dependency_health_and_compatibility",
        23: "observability_and_audit_trails",
        24: "experiment_and_safe_optimization",
        25: "multi_agent_consensus",
        26: "rollback_and_checkpoint_orchestration",
        27: "long_horizon_memory_and_knowledge",
        28: "goal_graph_and_dependency_planning",
        29: "resilient_continuous_operation",
        30: "self_governing_closed_loop_master_agent",
    })

    ADVANCED_PHASES = [
        "self_verify", "learn_failures", "recover", "deduplicate", "optimize",
        "secure", "check_dependencies", "observe", "experiment", "consensus",
        "checkpoint", "remember", "goal_graph", "resilience", "govern",
    ]

    SAFETY_POLICY = {
        "owner_approval_required": True,
        "real_world_changes_allowed": False,
        "sandbox_only": True,
        "arbitrary_generated_code_execution": False,
        "external_side_effects": False,
    }

    def _learn(self, mission, success, evidence=None):
        """Record learning without double-advancing the generation."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mission": mission["id"],
            "success": bool(success),
            "generation": self.state["generation"],
            "evidence": evidence or {},
            "quality_gate": "passed" if success else "not_passed",
        }
        self.state["learning"].append(event)
        self.state["learning"] = self.state["learning"][-200:]
        return event

    def advanced_capabilities(self) -> Dict[str, Any]:
        return {
            "generation_range": [16, 30],
            "features": [self.GENERATIONS[n] for n in range(16, 31)],
            "safety": dict(self.SAFETY_POLICY),
            "advanced_phases": list(self.ADVANCED_PHASES),
        }

    def quality_gate(self, test_passed=None, verification_passed=None):
        if test_passed is not True:
            return {"passed": False, "reason": "trusted_test_not_passed"}
        if verification_passed is not True:
            return {"passed": False, "reason": "independent_verification_not_passed"}
        return {"passed": True, "reason": "test_and_verification_passed"}

    def resilience_decision(self, failures: int, repeated_failure: bool = False):
        if repeated_failure:
            action = "checkpoint_rollback_and_replan"
        elif failures > 0:
            action = "repair_in_sandbox_and_retest"
        else:
            action = "continue"
        return {
            "action": action,
            "safe": True,
            "owner_approval_required": True,
            "real_world_changes_allowed": False,
        }

    def governance_status(self):
        return {
            "master_core": True,
            "version": self.VERSION,
            "max_generation": self.MAX_GENERATION,
            "generation_catalog_complete": len(self.GENERATIONS) == 30,
            "owner_approval_required": True,
            "real_world_changes_allowed": False,
            "sandbox_only": True,
            "arbitrary_generated_code_execution": False,
        }

    def status(self):
        result = super().status()
        result.update({
            "version": self.VERSION,
            "max_generation": self.MAX_GENERATION,
            "generation_16_30": {str(k): v for k, v in self.GENERATIONS.items() if k >= 16},
            "advanced_phases": list(self.ADVANCED_PHASES),
            "safety": dict(self.SAFETY_POLICY),
        })
        return result
