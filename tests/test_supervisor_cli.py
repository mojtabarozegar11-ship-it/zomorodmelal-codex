import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SupervisorCliTests(unittest.TestCase):
    def test_help_exposes_safe_runtime_controls(self):
        result = subprocess.run(
            [sys.executable, "-m", "autonomous_core.supervisor", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("--goal", result.stdout)
        self.assertIn("--interval", result.stdout)
        self.assertIn("--once", result.stdout)
        self.assertIn("--stop", result.stdout)
        self.assertIn("--status", result.stdout)

    def test_status_command_returns_json_safety_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # The CLI itself uses the repository root; exercise the equivalent
            # read-only status contract directly with an isolated supervisor.
            from autonomous_core.supervisor import AutonomousSupervisor
            supervisor = AutonomousSupervisor(root)
            supervisor.set_desired_state("stopped")
            status = supervisor.status()
            self.assertEqual(status["desired_state"], "stopped")
            self.assertTrue(status["owner_approval_required"])
            self.assertFalse(status["real_changes_allowed"])

    def test_stop_command_is_read_only_with_respect_to_external_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            from autonomous_core.supervisor import AutonomousSupervisor
            supervisor = AutonomousSupervisor(root)
            supervisor.set_desired_state("stopped")
            status = supervisor.status()
            self.assertEqual(status["status"], "stopped")
            self.assertFalse(status["real_changes_allowed"])


if __name__ == "__main__":
    unittest.main()
