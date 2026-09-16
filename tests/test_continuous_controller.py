import tempfile
import unittest
from pathlib import Path

from autonomous_core.continuous_controller import ContinuousController


class ContinuousControllerTests(unittest.TestCase):
    def test_failed_cycle_enters_bounded_self_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = ContinuousController(Path(tmp))
            result = controller.observe({"report": {"cycle": 1, "phase": "test", "goal": "repair"}, "tests": {"passed": False}})
            self.assertEqual(result["action"], "self_repair")
            self.assertEqual(result["repair_attempts"], 1)
            self.assertTrue(controller.next_action()["automatic"])

    def test_approval_wait_does_not_consume_repair_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = ContinuousController(Path(tmp))
            result = controller.observe({"report": {"cycle": 2, "phase": "approval", "pending": ["approval:1:change_package_deploy"]}})
            self.assertEqual(result["action"], "wait_for_owner_approval")
            self.assertEqual(result["repair_attempts"], 0)
            self.assertFalse(controller.next_action()["automatic"])

    def test_repeated_failures_are_quarantined_after_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = ContinuousController(Path(tmp))
            for cycle in range(1, 4):
                controller.observe({"report": {"cycle": cycle, "phase": "test", "pending": []}, "tests": {"passed": False}})
            result = controller.observe({"report": {"cycle": 4, "phase": "test", "pending": []}, "tests": {"passed": False}})
            self.assertEqual(result["action"], "quarantine_and_escalate")
            self.assertEqual(result["repair_attempts"], 4)

    def test_success_resets_repair_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            controller = ContinuousController(Path(tmp))
            controller.observe({"report": {"cycle": 1, "phase": "test", "pending": []}, "tests": {"passed": False}})
            result = controller.observe({"report": {"cycle": 2, "phase": "evolve", "pending": []}, "tests": {"passed": True}})
            self.assertEqual(result["action"], "continue")
            self.assertEqual(result["repair_attempts"], 0)


if __name__ == "__main__":
    unittest.main()
