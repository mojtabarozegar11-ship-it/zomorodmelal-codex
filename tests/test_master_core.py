import os
import tempfile
import unittest

from autonomous_core.access_manager import AccessManager
from autonomous_core.agent_factory import AgentFactory
from autonomous_core.master_core import MasterCore


class MasterCoreSmokeTests(unittest.TestCase):
    def _core(self, tmp):
        core = MasterCore.__new__(MasterCore)
        core.root = tmp
        core.data_dir = os.path.join(tmp, "data")
        core.sandbox_dir = os.path.join(tmp, "sandbox", "autonomous_workspace")
        core.state_file = os.path.join(core.data_dir, "master_core_state.json")
        core.mission_file = os.path.join(core.data_dir, "master_mission_queue.json")
        core.discovery_file = os.path.join(core.data_dir, "project_discovery.json")
        core._discovery_cache = None
        core._discovery_cache_at = 0.0
        core._persisted_discovery_cache = None
        core._persisted_discovery_cache_at = 0.0
        core._hot_cache = None
        core._hot_cache_at = 0.0
        core.access_manager = AccessManager(tmp)
        core.agent_factory = AgentFactory(tmp)
        os.makedirs(core.data_dir, exist_ok=True)
        os.makedirs(core.sandbox_dir, exist_ok=True)
        core.state = core._defaults()
        return core

    def test_cycle_is_safe_and_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            result = core.run_cycle()
            self.assertEqual(result["cycle"], 1)
            self.assertTrue(result["owner_approval_required"] if "owner_approval_required" in result else result["safety"]["owner_approval_required"])
            self.assertFalse(result["real_changes_allowed"] if "real_changes_allowed" in result else result["safety"]["real_deployment"])
            self.assertTrue(result["sandbox_only"] if "sandbox_only" in result else result["safety"]["sandbox_only"])
            self.assertIn("next_mission", result)
            self.assertIn("learning", result)
            self.assertTrue(os.path.exists(core.mission_file))

    def test_mission_changes_when_repair_goal_is_given(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            result = core.run_cycle("اصلاح و تست مجدد")
            self.assertEqual(result["next_mission"]["id"], "quality.repair_and_retest")
            self.assertEqual(result["next_mission"]["priority"], 95)

    def test_proposals_are_replaced_not_accumulated(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            core.state["proposals"] = [{"old": True}]
            proposals = core.create_proposals(["planning"], [])
            self.assertEqual(len(proposals), 1)
            self.assertFalse(any(item.get("old") for item in proposals))

    def test_owner_gate_is_immutable_in_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            result = core.run_cycle("deploy to hosting")
            self.assertTrue(result["safety"]["owner_approval_required"])
            self.assertFalse(result["safety"]["real_deployment"])
            self.assertTrue(result["safety"]["sandbox_only"])


if __name__ == "__main__":
    unittest.main()
