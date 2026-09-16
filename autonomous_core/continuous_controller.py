from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Union

from autonomous_core.mission_executor import MissionExecutor


class ContinuousController:
    """Persistent closed-loop controller for safe autonomous operation."""

    MAX_REPAIR_ATTEMPTS = 3
    RETRY_DELAY_SECONDS = 1.0

    def __init__(self, root: Union[str, Path]) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / "data" / "continuous_controller.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.executor = MissionExecutor(self.root)

    def _load(self) -> Dict[str, Any]:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError, TypeError):
            return {}

    def _save(self, state: Dict[str, Any]) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def observe(self, result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        state = self._load()
        report = (result or {}).get("report", {})
        tests = (result or {}).get("tests") or {}
        passed = tests.get("passed") is True
        pending = list(report.get("pending", []) or [])
        if passed:
            attempts = 0
            action = "continue"
        elif report.get("phase") == "approval" or any(str(x).startswith("approval:") for x in pending):
            attempts = int(state.get("repair_attempts", 0))
            action = "wait_for_owner_approval"
        else:
            attempts = int(state.get("repair_attempts", 0)) + 1
            action = "self_repair" if attempts <= self.MAX_REPAIR_ATTEMPTS else "quarantine_and_escalate"

        execution = self.executor.execute_next()
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": report.get("cycle"),
            "goal": report.get("goal"),
            "action": action,
            "repair_attempts": attempts,
            "max_repair_attempts": self.MAX_REPAIR_ATTEMPTS,
            "tests_passed": passed,
            "pending": pending,
            "mission_execution": execution,
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "sandbox_only": True,
        }
        self._save(snapshot)
        return snapshot

    def next_action(self) -> Dict[str, Any]:
        state = self._load()
        action = state.get("action", "continue")
        execution = state.get("mission_execution") or {}
        return {
            "action": action,
            "repair_attempts": int(state.get("repair_attempts", 0)),
            "max_repair_attempts": self.MAX_REPAIR_ATTEMPTS,
            "retry_delay_seconds": self.RETRY_DELAY_SECONDS if action == "self_repair" else 0.0,
            "automatic": action in {"continue", "self_repair"},
            "mission_execution": execution,
            "owner_approval_required": True,
            "real_changes_allowed": False,
        }
