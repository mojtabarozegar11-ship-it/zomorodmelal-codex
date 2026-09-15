from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from controller.rollback_manager import RollbackManager


@dataclass(frozen=True)
class RollbackPolicy:
    enabled: bool = True
    automatic_rollback: bool = False
    owner_approval_required: bool = True


class AutonomousRollback:
    """Adds rollback readiness to the autonomous cycle without auto-rollback."""

    def __init__(self, root: str | None = None) -> None:
        self.manager = RollbackManager(root)
        self.policy = RollbackPolicy()

    def prepare(self, paths: List[str]) -> Dict[str, Any]:
        backup = self.manager.create_backup(paths)
        return {
            "backup": backup,
            "rollback_ready": True,
            "automatic_rollback": self.policy.automatic_rollback,
            "owner_approval_required": self.policy.owner_approval_required,
            "files": paths,
        }

    def restore(self, backup: str, paths: List[str], owner_approved: bool = False) -> Dict[str, Any]:
        if self.policy.owner_approval_required and not owner_approved:
            return {"success": False, "status": "approval_required"}
        return self.manager.rollback(backup, paths)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.policy.enabled,
            "rollback_ready": True,
            "automatic_rollback": self.policy.automatic_rollback,
            "owner_approval_required": self.policy.owner_approval_required,
        }
