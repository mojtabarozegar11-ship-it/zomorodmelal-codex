from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

from autonomous_core.autonomous_cycle import AutonomousCycle


class SupervisorAlreadyRunning(RuntimeError):
    """Raised when another supervisor instance owns the runtime lock."""


class AutonomousSupervisor:
    """Continuously advance safe autonomous cycles with a single-process lock."""

    def __init__(self, project_root: str | Path | None = None, interval_seconds: int = 60,
                 cycle_factory: Callable[[Path], AutonomousCycle] | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent).resolve()
        self.interval_seconds = max(1, int(interval_seconds))
        self.cycle_factory = cycle_factory or AutonomousCycle
        self.state_path = self.project_root / "data" / "supervisor_state.json"
        self.lock_path = self.project_root / "data" / "supervisor.lock"
        self.control_path = self.project_root / "data" / "supervisor_control.json"
        self.stop_requested = False
        self._lock_owned = False

    def request_stop(self) -> None:
        self.stop_requested = True

    def set_desired_state(self, desired_state: str) -> None:
        if desired_state not in {"running", "stopped"}:
            raise ValueError("desired_state must be running or stopped")
        self.control_path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.control_path.with_suffix(".tmp")
        temp.write_text(json.dumps({"desired_state": desired_state}, indent=2), encoding="utf-8")
        temp.replace(self.control_path)
        if desired_state == "stopped":
            self.stop_requested = True

    def desired_state(self) -> str:
        try:
            data = json.loads(self.control_path.read_text(encoding="utf-8"))
            return data.get("desired_state", "running")
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return "running"

    def _acquire_lock(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(str(os.getpid()))
            self._lock_owned = True
        except FileExistsError as exc:
            raise SupervisorAlreadyRunning("another supervisor instance is already running") from exc

    def _release_lock(self) -> None:
        if self._lock_owned:
            try:
                self.lock_path.unlink()
            except FileNotFoundError:
                pass
            self._lock_owned = False

    def _save_state(self, state: Dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.state_path.with_suffix(".tmp")
        temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.state_path)

    def _base_state(self, **values: Any) -> Dict[str, Any]:
        return {"owner_approval_required": True, "real_changes_allowed": False,
                "updated_at": datetime.now(timezone.utc).isoformat(), **values}

    def run_once(self, goal: str | None = None) -> Dict[str, Any]:
        try:
            result = self.cycle_factory(self.project_root).run(goal)
        except Exception as exc:
            self._save_state(self._base_state(status="error", blocked=True,
                                               error_type=type(exc).__name__, error=str(exc)))
            raise
        report = result.get("report", {})
        pending = report.get("pending", [])
        self._save_state(self._base_state(
            status="blocked" if pending else "running",
            last_cycle=report.get("cycle"), last_phase=report.get("phase"),
            last_goal=report.get("goal"), blocked=bool(pending), pending=pending))
        return result

    def run_forever(self, goal: str | None = None) -> None:
        self._acquire_lock()
        try:
            self.stop_requested = self.desired_state() == "stopped"
            while not self.stop_requested:
                try:
                    result = self.run_once(goal)
                except Exception:
                    time.sleep(self.interval_seconds)
                    continue
                report = result.get("report", {})
                pending = report.get("pending", [])
                if pending:
                    self._save_state(self._base_state(
                        status="waiting_owner_approval", last_cycle=report.get("cycle"),
                        last_phase=report.get("phase"), last_goal=report.get("goal"),
                        blocked=True, pending=pending))
                time.sleep(self.interval_seconds)
                if self.desired_state() == "stopped":
                    self.stop_requested = True
            self._save_state(self._base_state(status="stopped", blocked=False, pending=[]))
        finally:
            self._release_lock()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the safe autonomous supervisor")
    parser.add_argument("--goal", default=os.environ.get("MASTER_AGENT_GOAL"))
    parser.add_argument("--interval", type=int,
                        default=int(os.environ.get("SUPERVISOR_INTERVAL_SECONDS", "300")))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--stop", action="store_true", help="request a running supervisor to stop")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    supervisor = AutonomousSupervisor(interval_seconds=args.interval)
    if args.stop:
        supervisor.set_desired_state("stopped")
    elif args.once:
        supervisor.run_once(args.goal)
    else:
        supervisor.set_desired_state("running")
        supervisor.run_forever(args.goal)
