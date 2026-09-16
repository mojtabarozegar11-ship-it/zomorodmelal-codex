import tempfile
import unittest
from pathlib import Path

from autonomous_core.supervisor import AutonomousSupervisor, SupervisorAlreadyRunning


class LockTests(unittest.TestCase):
    def test_second_supervisor_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = AutonomousSupervisor(root)
            second = AutonomousSupervisor(root)
            first._acquire_lock()
            try:
                with self.assertRaises(SupervisorAlreadyRunning):
                    second._acquire_lock()
            finally:
                first._release_lock()

    def test_stop_control_is_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            supervisor = AutonomousSupervisor(root)
            supervisor.set_desired_state("stopped")
            self.assertEqual(supervisor.desired_state(), "stopped")
            self.assertTrue(supervisor.stop_requested)


if __name__ == "__main__":
    unittest.main()
