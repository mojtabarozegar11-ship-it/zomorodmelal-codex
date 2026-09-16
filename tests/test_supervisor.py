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
            state = (root / "data" / "supervisor_state.json").read_text(encoding="utf-8")
            self.assertIn('"blocked": true', state)
            self.assertIn('"owner_approval_required": true', state)
            self.assertIn('"real_changes_allowed": false', state)
            self.assertIn('"status": "blocked"', state)

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


if __name__ == "__main__":
    unittest.main()
