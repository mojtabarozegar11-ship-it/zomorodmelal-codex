from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List

from autonomous_core.master_core import MasterCore
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
    """Coordinates safe autonomous reasoning without performing real deployment.

    The cycle may inspect, plan and prepare proposals. Any external effect,
    credential use, deployment, or irreversible change remains behind the
    owner-approval boundary.
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

    def __init__(self) -> None:
        self.master = MasterCore()
        self.testing = TestingEngine()
        self.evolution = EvolutionEngine()
        self.evaluation = EvaluationEngine()

    def run(self) -> Dict[str, Any]:
        core = self.master.run_cycle()

        pending: List[str] = []
        completed = ["discover", "research", "plan"]

        if core.get("syntax_errors"):
            pending.append("fix_syntax_errors")
        else:
            completed.extend(["build", "test", "verify"])

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
            "safety": {
                "sandbox_only": True,
                "real_deployment": False,
                "owner_approval_required": True,
            },
        }


if __name__ == "__main__":
    import json

    print(json.dumps(AutonomousCycle().run(), ensure_ascii=False, indent=2))
