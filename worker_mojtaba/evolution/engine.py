"""Evolution engine with checkpoint-aware candidate evaluation."""

from dataclasses import dataclass
from typing import Any

from worker_mojtaba.security.recovery import RecoveryManager


@dataclass
class CandidateVersion:
    version: str
    changes: list[str]
    status: str = "candidate"
    checkpoint_id: str | None = None
    rollback_state: dict[str, Any] | None = None


class EvolutionEngine:
    def __init__(self, recovery: RecoveryManager | None = None) -> None:
        self.recovery = recovery or RecoveryManager()

    def propose(self, current_version: str, improvements: list[str]) -> CandidateVersion:
        checkpoint_id = f"{current_version}-pre-upgrade"
        checkpoint = self.recovery.checkpoint(
            checkpoint_id,
            {"version": current_version, "changes": list(improvements)},
        )
        return CandidateVersion(
            version=f"{current_version}-candidate",
            changes=list(improvements),
            checkpoint_id=checkpoint.checkpoint_id,
            rollback_state=dict(checkpoint.state),
        )

    def evaluate(self, candidate: CandidateVersion, tests_passed: bool) -> CandidateVersion:
        candidate.status = "approved" if tests_passed else "rejected"
        return candidate

    def rollback(self, candidate: CandidateVersion) -> dict[str, Any]:
        if not candidate.checkpoint_id:
            raise ValueError("candidate has no rollback checkpoint")
        return self.recovery.restore(candidate.checkpoint_id)
