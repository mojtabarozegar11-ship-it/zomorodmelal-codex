import json
import tempfile
import unittest
from pathlib import Path

from autonomous_core.supervisor import AutonomousSupervisor, SupervisorAlreadyRunning


class FakeCycle:
    calls = 0

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, goal=None):
        type(self).calls += 1
        return {
            "report": {
                "cycle": type(self).calls,
                "phase": "approval",
                "goal": goal,
                "pending": ["owner_approval_for_real_changes"],
            }
        }


class SafeCycle(FakeCycle):
    def run(self, goal=None):
        type(self).calls += 1
        return {
            "report": {
                "cycle": type(self).calls,
                "phase": "learn",
                "goal": goal,
                "pending": [],
            }
        }


class FailingCycle:
    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, goal=None):
        raise RuntimeError("test failure")


class SupervisorTests(unittest.TestCase):
    def test_run_once_persists_safe_blocked_state(self):
        FakeCycle.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            result = supervisor.run_once("research market")
            self.assertEqual(result["report"]["cycle"], 1)
            self.assertEqual(result["mission_executor"]["status"], "idle")
            state = (root / "data" / "supervisor_state.json").read_text(encoding="utf-8")
            self.assertIn('"blocked": true', state)
            self.assertIn('"owner_approval_required": true', state)
            self.assertIn('"real_changes_allowed": false', state)
            self.assertIn('"status": "blocked"', state)

    def test_run_once_executes_safe_queued_mission_before_cycle(self):
        SafeCycle.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=SafeCycle)
            supervisor.mission_executor.queue.enqueue({"id": "safe.followup", "type": "improvement", "status": "ready"})
            result = supervisor.run_once("research market")
            self.assertEqual(result["mission_executor"]["status"], "completed")
            self.assertEqual(result["report"]["cycle"], 1)
            self.assertFalse(result["mission_executor"]["real_world_changes"])

    def test_run_once_persists_error_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FailingCycle)
            with self.assertRaises(RuntimeError):
                supervisor.run_once("research market")
            state = (root / "data" / "supervisor_state.json").read_text(encoding="utf-8")
            self.assertIn('"status": "error"', state)
            self.assertIn('"blocked": true', state)
            self.assertIn('"error_type": "RuntimeError"', state)

    def test_second_supervisor_is_rejected_by_runtime_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            first._acquire_lock()
            try:
                second = AutonomousSupervisor(root, cycle_factory=FakeCycle)
                with self.assertRaises(SupervisorAlreadyRunning):
                    second._acquire_lock()
            finally:
                first._release_lock()

    def test_stop_control_is_persistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            self.assertEqual(supervisor.desired_state(), "running")
            supervisor.set_desired_state("stopped")
            self.assertEqual(supervisor.desired_state(), "stopped")
            self.assertTrue(supervisor.stop_requested)
            supervisor.set_desired_state("running")
            self.assertEqual(supervisor.desired_state(), "running")

    def test_status_is_read_only_and_reports_runtime_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            supervisor.run_once("research market")
            status = supervisor.status()
            self.assertEqual(status["status"], "blocked")
            self.assertEqual(status["last_goal"], "research market")
            self.assertTrue(status["blocked"])
            self.assertTrue(status["owner_approval_required"])
            self.assertFalse(status["real_changes_allowed"])
            self.assertIsInstance(status["pending"], list)
            self.assertTrue((root / "data" / "supervisor_state.json").exists())

    def test_status_handles_invalid_state_file_safely(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "supervisor_state.json").write_text("not-json", encoding="utf-8")
            status = AutonomousSupervisor(root).status()
            self.assertEqual(status["status"], "stopped")
            self.assertTrue(status["owner_approval_required"])
            self.assertFalse(status["real_changes_allowed"])

    def test_non_deployment_waiting_approval_does_not_freeze_safe_cycle(self):
        SafeCycle.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=SafeCycle)
            supervisor.approval.request("goal_execution", "safe sandbox goal")
            result = supervisor.run_once("research market")
            self.assertEqual(result["report"]["cycle"], 1)
            self.assertEqual(result["report"]["goal"], "research market")
            self.assertEqual(result["report"]["pending"], [])
            status = supervisor.status()
            self.assertFalse(status["blocked"])

    def test_deployment_waiting_approval_pauses_safe_cycle(self):
        FakeCycle.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root, cycle_factory=FakeCycle)
            supervisor.approval.request(
                "change_package_deploy", "promote approved package",
                {"package_id": "pkg-1"},
            )
            result = supervisor.run_once("research market")
            self.assertIsNone(result["report"]["cycle"])
            self.assertEqual(result["report"]["phase"], "approval")
            self.assertEqual(FakeCycle.calls, 0)
            self.assertIsNone(result["mission_executor"])
            self.assertTrue(supervisor.status()["blocked"])


if __name__ == "__main__":
    unittest.main()
