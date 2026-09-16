from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from approval.approval_gateway import ApprovalGateway
from autonomous_core.agent_orchestrator import AgentOrchestrator
from autonomous_core.autonomous_decision_engine import AutonomousDecisionEngine
from autonomous_core.change_package import ChangePackage
from autonomous_core.master_core import MasterCore
from autonomous_core.safe_builder import SafeBuilder
from autonomous_core.self_evolution_controller import SelfEvolutionController
from autonomous_core.site_builder import SiteFeatureBuilder
from autonomous_core.site_connector import SiteConnector
from evaluation.evaluation_engine import EvaluationEngine
from evolution.evolution_engine import EvolutionEngine
from testing.testing_engine import TestingEngine


@dataclass
class CycleReport:
    cycle: int
    phase: str
    goal: str | None
    completed: List[str]
    pending: List[str]
    owner_approval_required: bool
    real_changes_allowed: bool
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AutonomousCycle:
    PHASES = ("discover", "research", "plan", "build", "test", "verify", "approval", "deploy", "learn", "evolve")
    FULL_TEST_INTERVAL = 10
    DEEP_DISCOVERY_INTERVAL = 10
    SITE_CHECK_INTERVAL = 10
    TEST_CACHE_SECONDS = 120.0
    FAST_TEST_MODULES = ("tests.test_master_core", "tests.test_autonomous_cycle_goal")

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.source_root = Path(__file__).resolve().parent.parent
        self.master = MasterCore(self.project_root)
        self.testing = TestingEngine(self.project_root / "data" / "test_results.json")
        self.evolution = EvolutionEngine(self.project_root / "data" / "evolution_proposals.json")
        self.evaluation = EvaluationEngine()
        self.self_evolution = SelfEvolutionController(self.project_root)
        self.approval = ApprovalGateway(self.project_root)
        self.packages = ChangePackage(self.project_root / "data" / "change_packages")
        self.site_builder = SiteFeatureBuilder()
        self.site_connector = SiteConnector(self.project_root)
        self.decision_engine = AutonomousDecisionEngine(self.project_root)
        self.orchestrator = AgentOrchestrator(self.project_root)
        self.test_cache_file = self.project_root / "data" / "autonomous_test_cache.json"

    @staticmethod
    def _read_json(path: Path) -> Dict[str, Any] | None:
        try:
            if path.exists():
                value = json.loads(path.read_text(encoding="utf-8"))
                return value if isinstance(value, dict) else None
        except (OSError, ValueError, TypeError):
            return None
        return None

    def _persist_project_discovery(self, core: Dict[str, Any], force: bool = False) -> Dict[str, Any] | None:
        path = self.project_root / "data" / "project_discovery.json"
        if not force:
            cached = self._read_json(path)
            if cached is not None:
                return cached
        files = []
        audits = {x["file"]: x for x in self.master.audit_python()}
        for relative in self.master.discover_project():
            item: Dict[str, Any] = {"path": relative}
            if relative.endswith(".py"):
                item["syntax_ok"] = bool(audits.get(relative, {}).get("syntax_ok"))
            files.append(item)
        snapshot = {"generated_at": datetime.now(timezone.utc).isoformat(), "root": str(self.project_root), "files": files,
                    "django_detected": any("django" in str(x).lower() for x in core.get("capabilities", [])),
                    "owner_approval_required": True, "real_changes_allowed": False}
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)
        return snapshot

    def _site_snapshot(self, cycle: int) -> Dict[str, Any]:
        path = self.project_root / "data" / "site_discovery.json"
        cached = self._read_json(path)
        if cached is not None and cycle % self.SITE_CHECK_INTERVAL != 0:
            return cached
        return self.site_connector.discover()

    def _sandbox_build(self, core: Dict[str, Any], goal: str | None) -> Dict[str, Any]:
        sandbox = self.project_root / "data" / "sandbox" / f"cycle_{core['cycle']}"
        builder = SafeBuilder(sandbox)
        files: Dict[str, str] = {"cycle_manifest.json": json.dumps({
            "cycle": core["cycle"], "goal": goal, "generated_at": datetime.now(timezone.utc).isoformat(),
            "capabilities": core.get("capabilities", []), "owner_approval_required": True, "real_changes_allowed": False}, ensure_ascii=False, indent=2)}
        if goal and any(x in goal.lower() for x in ("سایت", "وب", "website", "site")):
            files.update(self.site_builder.build(goal))
        return {"sandbox": str(sandbox), "files": builder.build(files)}

    def _test_modules_for_cycle(self, cycle: int) -> List[str]:
        override = os.environ.get("AUTONOMOUS_FULL_TESTS", "").strip().lower()
        if override in {"1", "true", "yes", "on"} or cycle % self.FULL_TEST_INTERVAL == 0:
            return []
        return list(self.FAST_TEST_MODULES)

    def _test_fingerprint(self, goal: str | None) -> str:
        h = hashlib.sha256(str(goal or "").encode("utf-8"))
        snapshot = self._read_json(self.project_root / "data" / "project_discovery.json") or {}
        paths = [x.get("path") for x in snapshot.get("files", []) if isinstance(x, dict) and x.get("path")]
        for relative in sorted(paths):
            try:
                stat = (self.project_root / relative).stat()
                h.update(relative.encode("utf-8"))
                h.update(str(stat.st_mtime_ns).encode("ascii"))
                h.update(str(stat.st_size).encode("ascii"))
            except OSError:
                h.update((relative + ":missing").encode("utf-8"))
        return h.hexdigest()

    def _cached_test(self, fingerprint: str, cycle: int) -> Dict[str, Any] | None:
        if cycle % self.FULL_TEST_INTERVAL == 0 or os.environ.get("AUTONOMOUS_FULL_TESTS", "").strip().lower() in {"1", "true", "yes", "on"}:
            return None
        cached = self._read_json(self.test_cache_file)
        if not cached or cached.get("fingerprint") != fingerprint or not cached.get("passed"):
            return None
        try:
            age = datetime.now(timezone.utc).timestamp() - float(cached.get("timestamp", 0))
        except (TypeError, ValueError):
            return None
        if age < 0 or age > self.TEST_CACHE_SECONDS:
            return None
        result = dict(cached.get("result") or {})
        result.update({"cached": True, "scope": "cached regression result"})
        return result

    def _store_test(self, fingerprint: str, result: Dict[str, Any]) -> None:
        if not result.get("passed"):
            return
        self.test_cache_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {"timestamp": datetime.now(timezone.utc).timestamp(), "fingerprint": fingerprint, "passed": True, "result": result}
        tmp = self.test_cache_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.test_cache_file)

    def _run_tests(self, cycle: int = 0, goal: str | None = None) -> Dict[str, Any]:
        fingerprint = self._test_fingerprint(goal)
        cached = self._cached_test(fingerprint, cycle)
        if cached is not None:
            return cached
        env = os.environ.copy()
        env["AUTONOMOUS_CYCLE_INNER_TESTS"] = "1"
        modules = self._test_modules_for_cycle(cycle)
        command = [sys.executable, "-m", "unittest"]
        if modules:
            command.extend(modules)
            scope = "fast regression suite"
        else:
            command.extend(["discover", "-s", "tests"])
            scope = "full test suite"
        try:
            completed = subprocess.run(command, cwd=self.source_root, capture_output=True, text=True, timeout=30, shell=False, env=env)
            result = {"passed": completed.returncode == 0, "returncode": completed.returncode,
                      "stdout": completed.stdout[-8000:], "stderr": completed.stderr[-8000:],
                      "failure_kind": "test_failure" if completed.returncode else "none", "scope": scope, "modules": modules, "cached": False}
        except subprocess.TimeoutExpired as exc:
            result = {"passed": False, "returncode": None, "stdout": str(exc.stdout or "")[-8000:],
                      "stderr": "test suite timed out after 30 seconds", "failure_kind": "timeout", "scope": scope, "modules": modules, "cached": False}
        self._store_test(fingerprint, result)
        return result

    def _repair_mission(self, goal: str | None, test_result: Dict[str, Any], cycle: int) -> Dict[str, Any]:
        plan = self.orchestrator.route(f"repair: {goal or 'autonomous test failure'}")
        mission = {"cycle": cycle, "type": "self_repair", "status": "queued_for_sandbox_repair", "goal": goal,
                   "failure_kind": test_result.get("failure_kind"), "returncode": test_result.get("returncode"),
                   "stdout": str(test_result.get("stdout", ""))[-8000:], "stderr": str(test_result.get("stderr", ""))[-8000:],
                   "agent_plan": plan, "owner_approval_required": True, "real_world_changes": False,
                   "created_at": datetime.now(timezone.utc).isoformat()}
        path = self.project_root / "data" / "self_repair_mission.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(mission, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)
        return mission

    def run(self, goal: str | None = None) -> Dict[str, Any]:
        core = self.master.run_cycle(goal)
        cycle = core["cycle"]
        self._persist_project_discovery(core, force=cycle % self.DEEP_DISCOVERY_INTERVAL == 0)
        site_snapshot = self._site_snapshot(cycle)
        decision = self.decision_engine.assess()
        effective_goal = goal or decision.get("decision")
        agent_plan = self.orchestrator.route(effective_goal)
        pending: List[str] = []
        completed = ["discover", "research", "plan", "agent_orchestration"]
        build_result = test_result = package = approval_request = repair_mission = None
        if core.get("syntax_errors"):
            repair_mission = self._repair_mission(effective_goal, {"failure_kind": "syntax_error"}, cycle)
            pending.append("fix_syntax_errors")
        else:
            try:
                build_result = self._sandbox_build(core, effective_goal)
                completed.append("build")
                test_result = self._run_tests(cycle, effective_goal)
                self.testing.record_test(f"autonomous_cycle_{cycle}", test_result["passed"], "Sandbox build plus adaptive autonomous regression testing.", diagnostics=test_result)
                if test_result["passed"]:
                    completed.extend(["test", "verify"])
                    sandbox_rel = str(Path(build_result["sandbox"]).relative_to(self.project_root))
                    package = self.packages.create(build_result["files"], f"Autonomous cycle {cycle} verified sandbox change set", sandbox_rel=sandbox_rel)
                    approval_request = self.approval.request("change_package_deploy", f"انتقال بسته تغییر چرخه {cycle} به محیط اصلی",
                        metadata={"package_id": package["package_id"], "package_sha256": package["package_sha256"], "cycle": cycle, "goal": effective_goal})
                    if approval_request.get("status") == "waiting_approval":
                        pending.append(f"approval:{approval_request['id']}:change_package_deploy")
                    elif approval_request.get("status") == "approved":
                        completed.append("approval_already_granted")
                else:
                    repair_mission = self._repair_mission(effective_goal, test_result, cycle)
                    pending.append("self_repair")
            except (OSError, TypeError, ValueError) as exc:
                repair_mission = self._repair_mission(effective_goal, {"failure_kind": "build_error", "stderr": str(exc)}, cycle)
                pending.append(f"build_error: {exc}")
        evolution = self.self_evolution.evaluate(test_result, len(self.orchestrator.factory.list_agents()))
        completed.extend(["learn", "evolve"])
        report = CycleReport(cycle, "approval" if any(p.startswith("approval:") for p in pending) else ("test" if pending else "evolve"),
                             effective_goal, completed, pending, True, False, datetime.now(timezone.utc).isoformat())
        return {"report": report.to_dict(), "core": core, "site": site_snapshot, "decision": decision, "agents": agent_plan,
                "build": build_result, "tests": test_result, "repair_mission": repair_mission, "evolution": evolution,
                "package": package, "approval_request": approval_request,
                "safety": {"sandbox_only": True, "generated_code_executed": False, "remote_site_write": False, "real_deployment": False, "owner_approval_required": True}}


if __name__ == "__main__":
    print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
