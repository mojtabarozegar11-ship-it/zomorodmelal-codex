from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from approval.approval_gateway import ApprovalGateway
from autonomous_core.change_package import ChangePackage
from autonomous_core.master_core import MasterCore
from autonomous_core.safe_builder import SafeBuilder
from autonomous_core.site_builder import SiteFeatureBuilder
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
    """Run a safe autonomous cycle and produce an approval-bound package."""
    PHASES = ("discover", "research", "plan", "build", "test", "verify", "approval", "deploy", "learn")

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.source_root = Path(__file__).resolve().parent.parent
        self.master = MasterCore(self.project_root)
        self.testing = TestingEngine()
        self.evolution = EvolutionEngine()
        self.evaluation = EvaluationEngine()
        self.approval = ApprovalGateway(self.project_root)
        self.packages = ChangePackage(self.project_root / "data" / "change_packages")
        self.site_builder = SiteFeatureBuilder()

    def _sandbox_build(self, core: Dict[str, Any], goal: str | None) -> Dict[str, Any]:
        sandbox = self.project_root / "data" / "sandbox" / f"cycle_{core['cycle']}"
        builder = SafeBuilder(sandbox)
        files: Dict[str, str] = {
            "cycle_manifest.json": json.dumps({
                "cycle": core["cycle"], "goal": goal,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "capabilities": core.get("capabilities", []),
                "owner_approval_required": True, "real_changes_allowed": False,
            }, ensure_ascii=False, indent=2)
        }
        if goal and any(x in goal.lower() for x in ("سایت", "وب", "website", "site")):
            files.update(self.site_builder.build(goal))
        return {"sandbox": str(sandbox), "files": builder.build(files)}

    def _run_tests(self) -> Dict[str, Any]:
        # The cycle may use an isolated temporary project root in tests. Run the
        # repository's test suite from the source tree while keeping all cycle
        # artifacts (sandbox/state/packages) under the requested project root.
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"]
        try:
            completed = subprocess.run(
                command,
                cwd=self.source_root,
                capture_output=True,
                text=True,
                timeout=90,
                shell=False,
            )
            return {
                "passed": completed.returncode == 0,
                "returncode": completed.returncode,
                "stdout": completed.stdout[-4000:],
                "stderr": completed.stderr[-4000:],
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "passed": False,
                "returncode": None,
                "stdout": (exc.stdout or "")[-4000:],
                "stderr": "test suite timed out after 90 seconds",
            }

    def run(self, goal: str | None = None) -> Dict[str, Any]:
        core = self.master.run_cycle(goal)
        pending: List[str] = []
        completed = ["discover", "research", "plan"]
        build_result = test_result = package = approval_request = None
        if core.get("syntax_errors"):
            pending.append("fix_syntax_errors")
        else:
            try:
                build_result = self._sandbox_build(core, goal)
                completed.append("build")
                test_result = self._run_tests()
                self.testing.record_test(f"autonomous_cycle_{core['cycle']}", test_result["passed"], "Sandbox build plus project unittest discovery.")
                if test_result["passed"]:
                    completed.extend(["test", "verify"])
                    sandbox_rel = str(Path(build_result["sandbox"]).relative_to(self.project_root))
                    package = self.packages.create(build_result["files"], f"Autonomous cycle {core['cycle']} verified sandbox change set", sandbox_rel=sandbox_rel)
                    approval_request = self.approval.request("change_package_deploy", f"انتقال بسته تغییر چرخه {core['cycle']} به محیط اصلی",
                        metadata={"package_id": package["package_id"], "package_sha256": package["package_sha256"], "cycle": core["cycle"], "goal": goal})
                else:
                    pending.append("fix_failing_tests")
            except (OSError, TypeError, ValueError) as exc:
                pending.append(f"build_error: {exc}")
        pending.extend(["owner_approval_for_real_changes", "controlled_deployment", "post_deployment_learning"])
        report = CycleReport(core["cycle"], "approval", goal, completed, pending, True, False, datetime.now(timezone.utc).isoformat())
        return {"report": report.to_dict(), "core": core, "build": build_result, "tests": test_result,
                "package": package, "approval_request": approval_request,
                "safety": {"sandbox_only": True, "generated_code_executed": False, "real_deployment": False, "owner_approval_required": True}}


if __name__ == "__main__":
    print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
