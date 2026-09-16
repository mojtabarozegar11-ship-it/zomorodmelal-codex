from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

from approval.approval_gateway import ApprovalGateway
from autonomous_core.autonomous_cycle import AutonomousCycle
from controller.change_package_executor import ChangePackageExecutor


class SupervisorAlreadyRunning(RuntimeError):
    """Raised when another supervisor instance owns the runtime lock."""


class AutonomousSupervisor:
    """Continuously advance safe autonomous cycles with observable runtime health."""

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
        self.approval = ApprovalGateway(self.project_root)
        self.package_executor = ChangePackageExecutor(self.project_root)

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

    def status(self) -> Dict[str, Any]:
        state: Dict[str, Any] = {}
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass
        lock_exists = self.lock_path.exists()
        status = state.get("status", "stopped")
        if lock_exists and status == "stopped":
            status = "starting"
        return {
            "status": status,
            "desired_state": self.desired_state(),
            "lock_present": lock_exists,
            "pid": state.get("pid"),
            "last_cycle": state.get("last_cycle"),
            "last_phase": state.get("last_phase"),
            "last_goal": state.get("last_goal"),
            "last_error": state.get("error"),
            "updated_at": state.get("updated_at"),
            "blocked": bool(state.get("blocked", False)),
            "pending": state.get("pending", []),
            "owner_approval_required": True,
            "real_changes_allowed": False,
        }

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
        return {
            "owner_approval_required": True,
            "real_changes_allowed": False,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **values,
        }

    def _waiting_approvals(self) -> list[Dict[str, Any]]:
        return self.approval.get_waiting()

    def _resume_approved_packages(self) -> list[Dict[str, Any]]:
        """Execute only already-approved package promotions."""
        results: list[Dict[str, Any]] = []
        for request in self.approval.get_all():
            if request.get("action") != "change_package_deploy" or request.get("status") != "approved":
                continue
            metadata = request.get("metadata") or {}
            package_id = metadata.get("package_id")
            if not package_id:
                continue
            results.append(self.package_executor.execute(package_id, int(request["id"])))
        return results

    def run_once(self, goal: str | None = None) -> Dict[str, Any]:
        """Run one safe cycle even when an older deployment approval is waiting.

        Approval remains mandatory for real deployment. A pending approval is
        reported as pending state, but it does not freeze unrelated sandbox work.
        """
        promoted = self._resume_approved_packages()
        waiting = self._waiting_approvals()
        pending_before_cycle = [
            f"approval:{r.get('id')}:{r.get('action')}" for r in waiting
            if r.get("action") == "change_package_deploy"
        ]

        try:
            result = self.cycle_factory(self.project_root).run(goal)
        except Exception as exc:
            self._save_state(self._base_state(
                status="error", blocked=True, error_type=type(exc).__name__,
                error=str(exc), pid=os.getpid(), pending=pending_before_cycle,
            ))
            raise

        report = result.get("report", {})
        cycle_pending = report.get("pending", [])
        all_pending = list(dict.fromkeys(pending_before_cycle + list(cycle_pending)))
        self._save_state(self._base_state(
            status="running",
            pid=os.getpid(),
            last_cycle=report.get("cycle"),
            last_phase=report.get("phase"),
            last_goal=report.get("goal"),
            blocked=False,
            pending=all_pending,
            approval_pending=bool(all_pending),
            resumed=promoted,
        ))
        return result

    def run_forever(self, goal: str | None = None) -> None:
        self._acquire_lock()
        try:
            self.stop_requested = self.desired_state() == "stopped"
            self._save_state(self._base_state(status="starting", pid=os.getpid(), blocked=False, pending=[]))
            while not self.stop_requested:
                try:
                    self.run_once(goal)
                except Exception:
                    time.sleep(self.interval_seconds)
                    if self.desired_state() == "stopped":
                        self.stop_requested = True
                    continue
                time.sleep(self.interval_seconds)
                if self.desired_state() == "stopped":
                    self.stop_requested = True
            self._save_state(self._base_state(status="stopped", pid=None, blocked=False, pending=[]))
        finally:
            self._release_lock()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the safe autonomous supervisor")
    parser.add_argument("--goal", default=os.environ.get("MASTER_AGENT_GOAL"))
    parser.add_argument("--interval", type=int,
                        default=int(os.environ.get("SUPERVISOR_INTERVAL_SECONDS", "300")))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--stop", action="store_true", help="request a running supervisor to stop")
    parser.add_argument("--status", action="store_true", help="show current supervisor runtime status")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    supervisor = AutonomousSupervisor(interval_seconds=args.interval)
    if args.status:
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.stop:
        supervisor.set_desired_state("stopped")
        print(json.dumps(supervisor.status(), ensure_ascii=False, indent=2))
    elif args.once:
        supervisor.run_once(args.goal)
    else:
        supervisor.set_desired_state("running")
        supervisor.run_forever(args.goal)
