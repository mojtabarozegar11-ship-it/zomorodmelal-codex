from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from .master_core import MasterCore


class MasterCore30(MasterCore):
    """Master Agent extension covering generations 16 through 30.

    This layer extends the existing generation-15 kernel without weakening its
    sandbox and owner-approval boundaries. It adds explicit quality control,
    resilience, governance, observability, optimization and long-horizon
    autonomy states. Real-world actions remain owner-gated.
    """

    VERSION = "30.0.0"
    MAX_GENERATION = 30
    GENERATIONS = dict(MasterCore.GENERATIONS, **{
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
        """Record learning without double-advancing the generation.

        The parent cycle performs the single generation transition after this
        method returns. Keeping the increment here disabled fixes the previous
        double-advance behavior.
        """
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
        """Return the explicit capabilities represented by generations 16-30."""
        return {
            "generation_range": [16, 30],
            "features": [self.GENERATIONS[n] for n in range(16, 31)],
            "safety": dict(self.SAFETY_POLICY),
            "advanced_phases": list(self.ADVANCED_PHASES),
        }

    def quality_gate(self, test_passed=None, verification_passed=None):
        """Require explicit evidence before a mission can be considered successful."""
        if test_passed is not True:
            return {"passed": False, "reason": "trusted_test_not_passed"}
        if verification_passed is not True:
            return {"passed": False, "reason": "independent_verification_not_passed"}
        return {"passed": True, "reason": "test_and_verification_passed"}

    def resilience_decision(self, failures: int, repeated_failure: bool = False):
        """Select a safe recovery mode; never authorize a real-world mutation."""
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
        """Expose the immutable governance boundary for generations 16-30."""
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
