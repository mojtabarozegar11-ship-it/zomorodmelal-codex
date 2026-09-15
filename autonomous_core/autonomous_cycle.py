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
from evaluation.evaluation_engine import EvaluationEngine
from evolution.evolution_engine import EvolutionEngine
from testing.testing_engine import TestingEngine


@dataclass
class CycleReport:
    cycle: int
    phase: str
    completed: List[str]
    pending: List[str]
    owner_approval_required: bool
    real_changes_allowed: bool
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AutonomousCycle:
    """Run a safe autonomous cycle and produce an approval-bound package."""

    PHASES = (
        "discover", "research", "plan", "build", "test", "verify",
        "approval", "deploy", "learn",
    )

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.master = MasterCore()
        self.testing = TestingEngine()
        self.evolution = EvolutionEngine()
        self.evaluation = EvaluationEngine()
        self.approval = ApprovalGateway()
        self.packages = ChangePackage(self.project_root / "data" / "change_packages")

    def _sandbox_build(self, core: Dict[str, Any]) -> Dict[str, Any]:
        sandbox = self.project_root / "data" / "sandbox" / f"cycle_{core['cycle']}"
        builder = SafeBuilder(sandbox)
        manifest = {
            "cycle_manifest.json": json.dumps(
                {
                    "cycle": core["cycle"],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "capabilities": core.get("capabilities", []),
                    "owner_approval_required": True,
                    "real_changes_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        }
        return {"sandbox": str(sandbox), "files": builder.build(manifest)}

    def _run_tests(self) -> Dict[str, Any]:
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"]
        try:
            completed = subprocess.run(
                command, cwd=self.project_root, capture_output=True,
                text=True, timeout=90, shell=False,
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

    def run(self) -> Dict[str, Any]:
        core = self.master.run_cycle()
        pending: List[str] = []
        completed = ["discover", "research", "plan"]
        build_result: Dict[str, Any] | None = None
        test_result: Dict[str, Any] | None = None
        package: Dict[str, Any] | None = None
        approval_request: Dict[str, Any] | None = None

        if core.get("syntax_errors"):
            pending.append("fix_syntax_errors")
        else:
            try:
                build_result = self._sandbox_build(core)
                completed.append("build")
                test_result = self._run_tests()
                self.testing.record_test(
                    f"autonomous_cycle_{core['cycle']}", test_result["passed"],
                    "Sandbox build plus project unittest discovery.",
                )
                if test_result["passed"]:
                    completed.extend(["test", "verify"])
                    sandbox_rel = str(Path(build_result["sandbox"]).relative_to(self.project_root))
                    package = self.packages.create(
                        build_result["files"],
                        f"Autonomous cycle {core['cycle']} verified sandbox change set",
                        sandbox_rel=sandbox_rel,
                    )
                    approval_request = self.approval.request(
                        "change_package_deploy",
                        f"انتقال بسته تغییر چرخه {core['cycle']} به محیط اصلی",
                        metadata={
                            "package_id": package["package_id"],
                            "package_sha256": package["package_sha256"],
                            "cycle": core["cycle"],
                        },
                    )
                else:
                    pending.append("fix_failing_tests")
            except (OSError, TypeError, ValueError) as exc:
                pending.append(f"build_error: {exc}")

        if approval_request:
            pending.extend(["owner_approval_for_real_changes", "controlled_deployment", "post_deployment_learning"])
        else:
            pending.extend(["owner_approval_for_real_changes", "controlled_deployment", "post_deployment_learning"])

        report = CycleReport(
            cycle=core["cycle"], phase="approval", completed=completed,
            pending=pending, owner_approval_required=True,
            real_changes_allowed=False, timestamp=datetime.now(timezone.utc).isoformat(),
        )

        return {
            "report": report.to_dict(),
            "core": core,
            "build": build_result,
            "tests": test_result,
            "package": package,
            "approval_request": approval_request,
            "safety": {
                "sandbox_only": True,
                "generated_code_executed": False,
                "real_deployment": False,
                "owner_approval_required": True,
            },
        }


if __name__ == "__main__":
    print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
