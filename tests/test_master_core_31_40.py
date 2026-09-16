import unittest

from autonomous_core.master_core_generation_31_40 import MasterCore40


class MasterCore3140Tests(unittest.TestCase):
    def test_generation_catalog(self):
        self.assertEqual(MasterCore40.MAX_GENERATION, 40)
        self.assertEqual(len(MasterCore40.GENERATIONS), 40)
        self.assertEqual(MasterCore40.GENERATIONS[40], "autonomous_operating_system_for_missions")

    def test_conservative_evidence_decision(self):
        core = MasterCore40.__new__(MasterCore40)
        self.assertEqual(core.evidence_decision({})["decision"], "collect_more_evidence")
        self.assertEqual(
            core.evidence_decision({"trusted_test_passed": True, "independent_verification_passed": True})["decision"],
            "continue",
        )

    def test_failure_containment(self):
        core = MasterCore40.__new__(MasterCore40)
        result = core.containment_decision(3)
        self.assertEqual(result["action"], "checkpoint_rollback_and_quarantine")
        self.assertTrue(result["owner_approval_required"])
        self.assertFalse(result["real_world_changes_allowed"])


if __name__ == "__main__":
    unittest.main()
