from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from approval.approval_gateway import ApprovalGateway
from autonomous_core.autonomous_decision_engine import AutonomousDecisionEngine
from autonomous_core.change_package import ChangePackage
from autonomous_core.master_core import MasterCore
from autonomous_core.safe_builder import SafeBuilder
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
    def to_dict(self) -> Dict[str, Any]: return asdict(self)

class AutonomousCycle:
    PHASES = ("discover", "research", "plan", "build", "test", "verify", "approval", "deploy", "learn")
    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.source_root = Path(__file__).resolve().parent.parent
        self.master = MasterCore(self.project_root)
        self.testing = TestingEngine(); self.evolution = EvolutionEngine(); self.evaluation = EvaluationEngine()
        self.approval = ApprovalGateway(self.project_root)
        self.packages = ChangePackage(self.project_root / "data" / "change_packages")
        self.site_builder = SiteFeatureBuilder(); self.site_connector = SiteConnector(self.project_root)
        self.decision_engine = AutonomousDecisionEngine(self.project_root)

    def _persist_project_discovery(self, core: Dict[str, Any]) -> None:
        files = []
        audits = {x["file"]: x for x in self.master.audit_python()}
        for relative in self.master.discover_project():
            item: Dict[str, Any] = {"path": relative}
            if relative.endswith(".py"): item["syntax_ok"] = bool(audits.get(relative, {}).get("syntax_ok"))
            files.append(item)
        snapshot = {"generated_at": datetime.now(timezone.utc).isoformat(), "root": str(self.project_root), "files": files, "django_detected": any("django" in str(x).lower() for x in core.get("capabilities", [])), "owner_approval_required": True, "real_changes_allowed": False}
        path = self.project_root / "data" / "project_discovery.json"; tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"); tmp.replace(path)

    def _sandbox_build(self, core: Dict[str, Any], goal: str | None) -> Dict[str, Any]:
        sandbox = self.project_root / "data" / "sandbox" / f"cycle_{core['cycle']}"
        builder = SafeBuilder(sandbox)
        files: Dict[str, str] = {"cycle_manifest.json": json.dumps({"cycle": core["cycle"], "goal": goal, "generated_at": datetime.now(timezone.utc).isoformat(), "capabilities": core.get("capabilities", []), "owner_approval_required": True, "real_changes_allowed": False}, ensure_ascii=False, indent=2)}
        if goal and any(x in goal.lower() for x in ("سایت", "وب", "website", "site")): files.update(self.site_builder.build(goal))
        return {"sandbox": str(sandbox), "files": builder.build(files)}

    def _run_tests(self) -> Dict[str, Any]:
        env = os.environ.copy(); env["AUTONOMOUS_CYCLE_INNER_TESTS"] = "1"
        try:
            completed = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=self.source_root, capture_output=True, text=True, timeout=90, shell=False, env=env)
            return {"passed": completed.returncode == 0, "returncode": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}
        except subprocess.TimeoutExpired as exc:
            return {"passed": False, "returncode": None, "stdout": (exc.stdout or "")[-4000:], "stderr": "test suite timed out after 90 seconds"}

    def run(self, goal: str | None = None) -> Dict[str, Any]:
        core = self.master.run_cycle(goal)
        self._persist_project_discovery(core)
        site_snapshot = self.site_connector.discover()
        decision = self.decision_engine.assess()
        effective_goal = goal or decision.get("decision")
        pending: List[str] = []; completed = ["discover", "research", "plan"]
        build_result = test_result = package = approval_request = None
        if core.get("syntax_errors"): pending.append("fix_syntax_errors")
        else:
            try:
                build_result = self._sandbox_build(core, effective_goal); completed.append("build")
                test_result = self._run_tests()
                self.testing.record_test(f"autonomous_cycle_{core['cycle']}", test_result["passed"], "Sandbox build plus project unittest discovery.")
                if test_result["passed"]:
                    completed.extend(["test", "verify"])
                    sandbox_rel = str(Path(build_result["sandbox"]).relative_to(self.project_root))
                    package = self.packages.create(build_result["files"], f"Autonomous cycle {core['cycle']} verified sandbox change set", sandbox_rel=sandbox_rel)
                    approval_request = self.approval.request("change_package_deploy", f"انتقال بسته تغییر چرخه {core['cycle']} به محیط اصلی", metadata={"package_id": package["package_id"], "package_sha256": package["package_sha256"], "cycle": core["cycle"], "goal": effective_goal})
                    if approval_request.get("status") == "waiting_approval": pending.append(f"approval:{approval_request['id']}:change_package_deploy")
                    elif approval_request.get("status") == "approved": completed.append("approval_already_granted")
                else: pending.append("fix_failing_tests")
            except (OSError, TypeError, ValueError) as exc: pending.append(f"build_error: {exc}")
        report = CycleReport(core["cycle"], "approval" if any(p.startswith("approval:") for p in pending) else ("test" if pending else "learn"), effective_goal, completed, pending, True, False, datetime.now(timezone.utc).isoformat())
        return {"report": report.to_dict(), "core": core, "site": site_snapshot, "decision": decision, "build": build_result, "tests": test_result, "package": package, "approval_request": approval_request, "safety": {"sandbox_only": True, "generated_code_executed": False, "remote_site_write": False, "real_deployment": False, "owner_approval_required": True}}

if __name__ == "__main__": print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
