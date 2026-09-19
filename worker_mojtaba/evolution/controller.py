"""Upgrade controller for checkpointed, test-gated evolution.

This controller orchestrates proposal, evaluation, and rollback state.
It does not deploy or mutate production automatically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from worker_mojtaba.evolution.engine import CandidateVersion, EvolutionEngine


@dataclass(frozen=True)
class UpgradeResult:
    candidate: CandidateVersion
    action: str
    state: dict[str, Any]


class UpgradeController:
    def __init__(self, evolution: EvolutionEngine | None = None) -> None:
        self.evolution = evolution or EvolutionEngine()

    def run(
        self,
        current_version: str,
        improvements: list[str],
        test_runner: Callable[[], bool],
    ) -> UpgradeResult:
        candidate = self.evolution.propose(current_version, improvements)
        tests_passed = bool(test_runner())
        self.evolution.evaluate(candidate, tests_passed)

        if candidate.status == "approved":
            return UpgradeResult(
                candidate=candidate,
                action="awaiting_owner_approval",
                state={"version": candidate.version, "checkpoint_id": candidate.checkpoint_id},
            )

        return UpgradeResult(
            candidate=candidate,
            action="rollback_available",
            state=self.evolution.rollback(candidate),
        )
