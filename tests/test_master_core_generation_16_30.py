import os
import tempfile
import unittest

from autonomous_core.master_core_generation_16_30 import MasterCore30


class MasterCore30Tests(unittest.TestCase):
    def test_catalog_reaches_generation_30(self):
        with tempfile.TemporaryDirectory() as root:
            core = MasterCore30(root)
            self.assertEqual(core.MAX_GENERATION, 30)
            self.assertEqual(len(core.GENERATIONS), 30)
            self.assertEqual(core.GENERATIONS[30], "self_governing_closed_loop_master_agent")

    def test_safety_boundary_is_immutable_in_extension(self):
        with tempfile.TemporaryDirectory() as root:
            core = MasterCore30(root)
            status = core.governance_status()
            self.assertTrue(status["owner_approval_required"])
            self.assertFalse(status["real_world_changes_allowed"])
            self.assertTrue(status["sandbox_only"])
            self.assertFalse(status["arbitrary_generated_code_execution"])

    def test_quality_gate_requires_both_test_and_verification(self):
        with tempfile.TemporaryDirectory() as root:
            core = MasterCore30(root)
            self.assertFalse(core.quality_gate(True, False)["passed"])
            self.assertTrue(core.quality_gate(True, True)["passed"])

    def test_resilience_stays_in_sandbox(self):
        with tempfile.TemporaryDirectory() as root:
            core = MasterCore30(root)
            decision = core.resilience_decision(2, repeated_failure=True)
            self.assertEqual(decision["action"], "checkpoint_rollback_and_replan")
            self.assertTrue(decision["safe"])
            self.assertFalse(decision["real_world_changes_allowed"])


if __name__ == "__main__":
    unittest.main()
