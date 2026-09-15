from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

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
    """Run a safe autonomous cycle with sandboxed build and verification.

    The cycle may inspect the project, prepare sandbox artifacts and run the
    project's existing test suite. It never deploys, uses credentials, or
    promotes sandbox changes without the owner-approval boundary.
    """

    PHASES = (
        "discover",
        "research",
        "plan",
        "build",
        "test",
        "verify",
        "approval",
        "deploy",
        "learn",
    )

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.master = MasterCore()
        self.testing = TestingEngine()
        self.evolution = EvolutionEngine()
        self.evaluation = EvaluationEngine()

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
        return {
            "sandbox": str(sandbox),
            "files": builder.build(manifest),
        }

    def _run_tests(self) -> Dict[str, Any]:
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"]
        try:
            completed = subprocess.run(
                command,
                cwd=self.project_root,
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

    def run(self) -> Dict[str, Any]:
        core = self.master.run_cycle()
        pending: List[str] = []
        completed = ["discover", "research", "plan"]
        build_result: Dict[str, Any] | None = None
        test_result: Dict[str, Any] | None = None

        if core.get("syntax_errors"):
            pending.append("fix_syntax_errors")
        else:
            try:
                build_result = self._sandbox_build(core)
                completed.append("build")
                test_result = self._run_tests()
                self.testing.record_test(
                    f"autonomous_cycle_{core['cycle']}",
                    test_result["passed"],
                    "Sandbox build plus project unittest discovery.",
                )
                if test_result["passed"]:
                    completed.extend(["test", "verify"])
                else:
                    pending.append("fix_failing_tests")
            except (OSError, TypeError, ValueError) as exc:
                pending.append(f"build_error: {exc}")

        pending.extend([
            "owner_approval_for_real_changes",
            "controlled_deployment",
            "post_deployment_learning",
        ])

        report = CycleReport(
            cycle=core["cycle"],
            phase="approval",
            completed=completed,
            pending=pending,
            owner_approval_required=True,
            real_changes_allowed=False,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        return {
            "report": report.to_dict(),
            "core": core,
            "build": build_result,
            "tests": test_result,
            "safety": {
                "sandbox_only": True,
                "generated_code_executed": False,
                "real_deployment": False,
                "owner_approval_required": True,
            },
        }


if __name__ == "__main__":
    print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
