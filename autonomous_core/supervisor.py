from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

from autonomous_core.autonomous_cycle import AutonomousCycle


class AutonomousSupervisor:
    """Continuously advance safe autonomous cycles without duplicating approvals."""

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

    def _base_state(self, **values: Any) -> Dict[str, Any]:
        return {
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **values,
        }

    def run_once(self, goal: str | None = None) -> Dict[str, Any]:
        try:
            result = self.cycle_factory(self.project_root).run(goal)
        except Exception as exc:
            self._save_state(self._base_state(
                status="error",
                blocked=True,
                error_type=type(exc).__name__,
                error=str(exc),
            ))
            raise

        report = result.get("report", {})
        pending = report.get("pending", [])
        blocked = bool(pending)
        self._save_state(self._base_state(
            status="blocked" if blocked else "running",
            last_cycle=report.get("cycle"),
            last_phase=report.get("phase"),
            last_goal=report.get("goal"),
            blocked=blocked,
            pending=pending,
        ))
        return result

    def run_forever(self, goal: str | None = None) -> None:
        current_goal = goal
        while not self.stop_requested:
            try:
                result = self.run_once(current_goal)
            except Exception:
                # Persisted error state is enough for an operator to inspect;
                # avoid a tight retry loop.
                time.sleep(self.interval_seconds)
                continue

            report = result.get("report", {})
            pending = report.get("pending", [])
            if pending:
                # Approval or another deliberate boundary means WAIT, not retry.
                self._save_state(self._base_state(
                    status="waiting_owner_approval",
                    last_cycle=report.get("cycle"),
                    last_phase=report.get("phase"),
                    last_goal=report.get("goal"),
                    blocked=True,
                    pending=pending,
                ))
                time.sleep(self.interval_seconds)
                continue

            time.sleep(self.interval_seconds)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the safe autonomous supervisor")
    parser.add_argument("--goal", default=os.environ.get("MASTER_AGENT_GOAL"), help="goal to advance")
    parser.add_argument(
        "--interval",
        type=int,
        default=int(os.environ.get("SUPERVISOR_INTERVAL_SECONDS", "300")),
        help="seconds between cycles (default: 300)",
    )
    parser.add_argument("--once", action="store_true", help="run exactly one cycle")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    supervisor = AutonomousSupervisor(interval_seconds=args.interval)
    if args.once:
        supervisor.run_once(args.goal)
    else:
        supervisor.run_forever(args.goal)
