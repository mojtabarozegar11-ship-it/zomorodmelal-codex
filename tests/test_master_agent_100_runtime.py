import tempfile
import unittest
from pathlib import Path

from autonomous_core.autonomous_cycle_100 import AutonomousCycle100
from autonomous_core.master_core_generation_41_100 import MasterAgent100


class MasterAgent100RuntimeTests(unittest.TestCase):
    def test_cycle_uses_master_agent_100(self):
        with tempfile.TemporaryDirectory() as tmp:
            cycle = AutonomousCycle100(Path(tmp))
            self.assertIsInstance(cycle.master, MasterAgent100)
            self.assertEqual(cycle.master.VERSION, "100.0.0")
            self.assertEqual(cycle.master.MAX_GENERATION, 100)

    def test_runtime_status_preserves_safety_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            status = AutonomousCycle100(Path(tmp)).runtime_status()
            self.assertEqual(status["master_version"], "100.0.0")
            self.assertEqual(status["max_generation"], 100)
            self.assertTrue(status["safety"]["owner_approval_required"])
            self.assertFalse(status["safety"]["real_changes_allowed"])
            self.assertTrue(status["safety"]["sandbox_only"])


if __name__ == "__main__":
    unittest.main()
