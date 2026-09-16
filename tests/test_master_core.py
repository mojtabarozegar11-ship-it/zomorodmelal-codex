import os
import tempfile
import unittest

from autonomous_core.access_manager import AccessManager
from autonomous_core.master_core import MasterCore


class MasterCoreSmokeTests(unittest.TestCase):
    def _core(self, tmp):
        core = MasterCore.__new__(MasterCore)
        core.root = tmp
        core.data_dir = os.path.join(tmp, "data")
        core.sandbox_dir = os.path.join(tmp, "sandbox", "autonomous_workspace")
        core.state_file = os.path.join(core.data_dir, "master_core_state.json")
        os.makedirs(core.data_dir, exist_ok=True)
        os.makedirs(core.sandbox_dir, exist_ok=True)
        core.access_manager = AccessManager(tmp)
        core.state = {
            "version": core.VERSION,
            "cycles": 0,
            "goals": [],
            "agents": [],
            "capabilities": [],
            "proposals": [],
            "access_requests": [],
            "last_cycle": None,
        }
        return core

    def test_cycle_is_safe_and_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            result = core.run_cycle()
            self.assertEqual(result["cycle"], 1)
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_changes_allowed"])
            self.assertTrue(result["sandbox_only"])
            self.assertIn("capabilities", result)
            self.assertIn("proposals", result)
            self.assertIn("access_requests", result)

    def test_access_requirements_are_metadata_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            core.state["capabilities"] = ["web_research", "execution_control"]
            requirements = core.discover_access_requirements()
            self.assertEqual({x["capability"] for x in requirements}, {"web_research"})
            self.assertTrue(all(x["owner_approval_required"] for x in requirements))
            self.assertTrue(all(not x["credentials_acquired"] for x in requirements))
            self.assertTrue(all(not x["activated"] for x in requirements))

    def test_proposals_are_replaced_not_accumulated(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = self._core(tmp)
            core.state["proposals"] = [{"old": True}]
            proposals = core.create_proposals(["planning"], [])
            self.assertEqual(len(proposals), 1)
            self.assertEqual(core.state["proposals"], proposals)
            self.assertFalse(any(item.get("old") for item in proposals))


if __name__ == "__main__":
    unittest.main()
