"""Audited wrapper for the weekly evolution upgrade controller."""

from __future__ import annotations

from typing import Any, Callable

from worker_mojtaba.evolution.controller import UpgradeController, UpgradeResult
from worker_mojtaba.security.audit import AuditLog


class AuditedUpgradeController:
    def __init__(
        self,
        controller: UpgradeController | None = None,
        audit: AuditLog | None = None,
    ) -> None:
        self.controller = controller or UpgradeController()
        self.audit = audit or AuditLog()

    def run(
        self,
        current_version: str,
        improvements: list[str],
        test_runner: Callable[[], bool],
    ) -> UpgradeResult:
        result = self.controller.run(current_version, improvements, test_runner)
        self.audit.record(
            "evolution_upgrade",
            result.candidate.status,
            {
                "current_version": current_version,
                "candidate_version": result.candidate.version,
                "changes": list(result.candidate.changes),
                "checkpoint_id": result.candidate.checkpoint_id,
                "action": result.action,
                "tests_passed": result.candidate.status == "approved",
            },
        )
        return result
