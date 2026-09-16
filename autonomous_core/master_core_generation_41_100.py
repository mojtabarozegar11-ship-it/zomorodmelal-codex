from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List

from .master_core_generation_31_40 import MasterCore40


class MasterCore100(MasterCore40):
    """Generations 41-100: integrated autonomous mission operating layer.

    This layer is deliberately deterministic at its control boundary. It can
    inspect, plan, score evidence, build safe work packages, test, learn and
    recover inside the sandbox. It never grants real-world authority.
    """

    VERSION = "100.0.0"
    MAX_GENERATION = 100

    GENERATIONS = dict(MasterCore40.GENERATIONS, **{
        41: "deep_self_audit",
        42: "failure_forecasting",
        43: "mission_dependency_management",
        44: "parallel_safe_workstreams",
        45: "specialist_agent_routing",
        46: "multi_source_evidence_fusion",
        47: "pre_action_policy_simulation",
        48: "adaptive_test_optimization",
        49: "failure_containment_budget",
        50: "closed_loop_operating_control",
        51: "architecture_self_mapping",
        52: "deep_root_cause_analysis",
        53: "predictive_mission_preparation",
        54: "dynamic_resource_capacity_management",
        55: "mission_conflict_resolution",
        56: "auditable_reasoning_evidence_chain",
        57: "multi_scenario_sandbox_simulation",
        58: "historical_failure_avoidance",
        59: "operational_cycle_self_tuning",
        60: "closed_loop_learning",
        61: "operational_self_audit",
        62: "bottleneck_detection",
        63: "capacity_forecasting",
        64: "intelligent_mission_scheduling",
        65: "dynamic_agent_allocation",
        66: "mission_conflict_resolution_v2",
        67: "execution_chain_optimization",
        68: "goal_drift_detection",
        69: "priority_self_adjustment",
        70: "closed_loop_operation_control",
        71: "long_term_experience_memory",
        72: "success_pattern_learning",
        73: "failure_pattern_learning_v2",
        74: "recurring_pattern_detection",
        75: "failure_prediction",
        76: "path_selection_learning",
        77: "inter_agent_knowledge_transfer",
        78: "reusable_knowledge_compilation",
        79: "knowledge_quality_evaluation",
        80: "knowledge_base_evolution",
        81: "multi_criteria_decision_engine",
        82: "alternative_scenario_comparison",
        83: "pre_execution_risk_analysis",
        84: "consequence_simulation",
        85: "evidence_first_decisions",
        86: "agent_consensus_protocol",
        87: "uncertainty_detection",
        88: "sensitive_action_approval_routing",
        89: "decision_trace_audit",
        90: "decision_retrospective",
        91: "ecosystem_agent_governance",
        92: "architecture_self_regulation",
        93: "controlled_self_repair",
        94: "continuous_self_optimization",
        95: "mission_lifecycle_management",
        96: "agent_lifecycle_management",
        97: "active_failure_prevention",
        98: "controlled_generation_evolution",
        99: "system_governance_and_control",
        100: "autonomous_master_agent_operating_system",
    })

    SAFETY_POLICY = {
        "owner_approval_required": True,
        "real_changes_allowed": False,
        "sandbox_only": True,
        "arbitrary_generated_code_execution": False,
        "external_side_effects": False,
    }

    CONTROL_PHASES = [
        "observe", "diagnose", "root_cause", "predict", "prioritize",
        "dependencies", "route_agents", "plan", "simulate_policy",
        "parallelize", "execute_sandbox", "adaptive_test", "repair",
        "verify", "weigh_evidence", "contain_failure", "learn",
        "evolve", "audit", "next_goal",
    ]

    def architecture_map(self, files: List[str]) -> Dict[str, Any]:
        groups: Dict[str, List[str]] = {}
        for path in files:
            root = path.replace('\\', '/').split('/')[0]
            groups.setdefault(root or '.', []).append(path)
        return {"file_count": len(files), "groups": groups}

    def root_cause(self, failures: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not failures:
            return {"root_cause": None, "confidence": 0.0, "evidence": []}
        kinds: Dict[str, int] = {}
        for item in failures:
            key = str(item.get("failure_kind") or item.get("type") or "unknown")
            kinds[key] = kinds.get(key, 0) + 1
        cause = sorted(kinds.items(), key=lambda pair: (-pair[1], pair[0]))[0][0]
        confidence = min(1.0, kinds[cause] / float(len(failures)))
        return {"root_cause": cause, "confidence": confidence, "evidence": failures[-20:]}

    def forecast_failure(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        failures = sum(1 for x in history if not x.get("success", False))
        total = len(history)
        rate = failures / float(total) if total else 0.0
        return {"failure_rate": rate, "risk": "high" if rate >= .5 else "medium" if rate >= .2 else "low"}

    def dependency_plan(self, missions: List[Dict[str, Any]]) -> Dict[str, Any]:
        seen = set()
        ordered = []
        for mission in missions:
            mid = str(mission.get("id", ""))
            if mid and mid not in seen:
                seen.add(mid)
                ordered.append(mid)
        return {"ordered_missions": ordered, "duplicates_removed": len(missions) - len(ordered)}

    def route_agent(self, mission: Dict[str, Any], agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        roles = set(mission.get("roles", []))
        candidates = [a for a in agents if a.get("role") in roles or a.get("name") in roles]
        return {"mission": mission.get("id"), "selected": candidates[:3], "fallback": not bool(candidates)}

    def fuse_evidence(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        trusted = [x for x in evidence if x.get("trusted") is True]
        passed = [x for x in trusted if x.get("passed") is True]
        failed = [x for x in trusted if x.get("passed") is False]
        if failed:
            decision = "repair_and_retest"
        elif passed:
            decision = "continue"
        else:
            decision = "collect_more_evidence"
        return {"decision": decision, "trusted_count": len(trusted), "passed_count": len(passed), "failed_count": len(failed)}

    def simulate_policy(self, action: str) -> Dict[str, Any]:
        sensitive = {"deploy", "publish", "payment", "external_action", "credential_change", "production_write"}
        needs_approval = action in sensitive
        return {**self.SAFETY_POLICY, "action": action, "simulated": True, "approval_required": needs_approval}

    def test_strategy(self, failure_kind: str = "") -> Dict[str, Any]:
        if failure_kind in {"syntax", "import", "runtime"}:
            tests = ["syntax", "unit", "integration"]
        elif failure_kind:
            tests = ["targeted", "unit", "regression"]
        else:
            tests = ["unit", "integration", "regression"]
        return {"strategy": tests, "safe": True}

    def containment(self, failures: int, budget: int = 3) -> Dict[str, Any]:
        remaining = max(0, int(budget) - int(failures))
        if failures >= budget:
            action = "rollback_and_quarantine"
        elif failures:
            action = "bounded_repair"
        else:
            action = "normal"
        return {"action": action, "remaining_budget": remaining, **self.SAFETY_POLICY}

    def decision(self, evidence: List[Dict[str, Any]], failures: List[Dict[str, Any]]) -> Dict[str, Any]:
        root = self.root_cause(failures)
        forecast = self.forecast_failure(self.state.get("learning", []))
        fused = self.fuse_evidence(evidence)
        if failures:
            action = "repair_and_retest"
        elif fused["decision"] == "continue":
            action = "continue"
        else:
            action = "collect_more_evidence"
        return {
            "action": action,
            "root_cause": root,
            "forecast": forecast,
            "evidence": fused,
            "safety": dict(self.SAFETY_POLICY),
        }

    def mission_fingerprint(self, mission: Dict[str, Any]) -> str:
        raw = "|".join(str(mission.get(k, "")) for k in ("id", "reason", "priority", "roles"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def operating_snapshot(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "generation": self.state.get("generation", 1),
            "phase": self.state.get("phase", "observe"),
            "cycles": self.state.get("cycles", 0),
            "goals": len(self.state.get("goals", [])),
            "agents": len(self.state.get("agents", [])),
            "capabilities": len(self.state.get("capabilities", [])),
            "pending_approvals": len(self.state.get("access_requests", [])),
            "safety": dict(self.SAFETY_POLICY),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def status(self):
        result = super().status()
        result.update({
            "version": self.VERSION,
            "max_generation": self.MAX_GENERATION,
            "generation_41_100": {str(k): v for k, v in self.GENERATIONS.items() if k >= 41},
            "control_phases": list(self.CONTROL_PHASES),
            "safety": dict(self.SAFETY_POLICY),
            "operating_snapshot": self.operating_snapshot(),
        })
        return result


MasterAgent100 = MasterCore100
