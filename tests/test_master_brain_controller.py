from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from autonomous_core.master_brain_controller import MasterBrainController


class MasterBrainControllerTests(unittest.TestCase):
    def test_plan_builds_sandbox_mission(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = MasterBrainController(Path(tmp))
            result = controller.plan("website security test")
            self.assertEqual(result["mission_status"], "planned")
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_world_actions"])
            self.assertGreaterEqual(len(result["route"]["agents"]), 1)

    def test_cycle_keeps_real_world_actions_gated(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = MasterBrainController(Path(tmp))
            result = controller.cycle("research agriculture")
            self.assertEqual(result["mission_status"], "sandbox_planned")
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_world_actions"])
            self.assertIn("next_step", result)

    def test_status_is_safe_when_idle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = MasterBrainController(Path(tmp)).status()
            self.assertEqual(result["status"], "idle")
            self.assertTrue(result["owner_approval_required"])


if __name__ == "__main__":
    unittest.main()
