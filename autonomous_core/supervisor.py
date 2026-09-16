from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

from autonomous_core.autonomous_cycle import AutonomousCycle


class AutonomousSupervisor:
    """Continuously advance safe autonomous cycles until stopped or blocked."""

    def __init__(
        self,
        project_root: str | Path | None = None,
        interval_seconds: int = 60,
        cycle_factory: Callable[[Path], AutonomousCycle] | None = None,
    ) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.interval_seconds = max(1, int(interval_seconds))
        self.cycle_factory = cycle_factory or AutonomousCycle
        self.state_path = self.project_root / "data" / "supervisor_state.json"
        self.stop_requested = False

    def request_stop(self) -> None:
        self.stop_requested = True

    def _save_state(self, state: Dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.state_path.with_suffix(".tmp")
        temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.state_path)

    def run_once(self, goal: str | None = None) -> Dict[str, Any]:
        result = self.cycle_factory(self.project_root).run(goal)
        report = result.get("report", {})
        blocked = bool(report.get("pending"))
        state = {
            "last_cycle": report.get("cycle"),
            "last_phase": report.get("phase"),
            "last_goal": report.get("goal"),
            "blocked": blocked,
            "pending": report.get("pending", []),
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save_state(state)
        return result

    def run_forever(self, goal: str | None = None) -> None:
        current_goal = goal
        while not self.stop_requested:
            result = self.run_once(current_goal)
            report = result.get("report", {})
            pending = report.get("pending", [])

            # A pending owner approval is a deliberate boundary, not an error.
            # Do not spin or repeatedly create identical sensitive actions.
            if "owner_approval_for_real_changes" in pending:
                time.sleep(self.interval_seconds)
                continue

            time.sleep(self.interval_seconds)


if __name__ == "__main__":
    AutonomousSupervisor().run_forever()
