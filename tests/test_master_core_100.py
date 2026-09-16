import tempfile
import unittest

from autonomous_core.master_core_generation_41_100 import MasterCore100


class MasterCore100Tests(unittest.TestCase):
    def make_core(self):
        return MasterCore100(tempfile.mkdtemp())

    def test_catalog_has_100_generations(self):
        core = self.make_core()
        self.assertEqual(core.MAX_GENERATION, 100)
        self.assertEqual(len(core.GENERATIONS), 100)
        self.assertEqual(core.GENERATIONS[100], "autonomous_master_agent_operating_system")

    def test_safety_policy_is_immutable_at_boundary(self):
        core = self.make_core()
        status = core.status()
        self.assertTrue(status["safety"]["owner_approval_required"])
        self.assertFalse(status["safety"]["real_changes_allowed"])
        self.assertTrue(status["safety"]["sandbox_only"])
        self.assertFalse(status["safety"]["arbitrary_generated_code_execution"])
        self.assertFalse(status["safety"]["external_side_effects"])

    def test_evidence_requires_more_when_untrusted(self):
        core = self.make_core()
        result = core.decision([{"trusted": False, "passed": True}], [])
        self.assertEqual(result["action"], "collect_more_evidence")

    def test_failure_routes_to_repair(self):
        core = self.make_core()
        result = core.decision([], [{"failure_kind": "syntax"}])
        self.assertEqual(result["action"], "repair_and_retest")
        self.assertEqual(result["root_cause"]["root_cause"], "syntax")

    def test_policy_simulation_never_grants_real_authority(self):
        core = self.make_core()
        result = core.simulate_policy("deploy")
        self.assertTrue(result["approval_required"])
        self.assertFalse(result["real_changes_allowed"])
        self.assertTrue(result["simulated"])

    def test_dependency_plan_deduplicates(self):
        core = self.make_core()
        result = core.dependency_plan([{"id": "a"}, {"id": "a"}, {"id": "b"}])
        self.assertEqual(result["ordered_missions"], ["a", "b"])
        self.assertEqual(result["duplicates_removed"], 1)

    def test_containment_is_bounded(self):
        core = self.make_core()
        result = core.containment(3, budget=3)
        self.assertEqual(result["action"], "rollback_and_quarantine")
        self.assertEqual(result["remaining_budget"], 0)
        self.assertFalse(result["real_changes_allowed"])

    def test_fingerprint_is_stable(self):
        core = self.make_core()
        mission = {"id": "x", "reason": "test", "priority": 50, "roles": ["testing"]}
        self.assertEqual(core.mission_fingerprint(mission), core.mission_fingerprint(mission))


if __name__ == "__main__":
    unittest.main()
