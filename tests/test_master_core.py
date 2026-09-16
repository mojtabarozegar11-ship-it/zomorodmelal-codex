import os
import tempfile
import unittest

from autonomous_core.access_manager import AccessManager
from autonomous_core.master_core import MasterCore


class MasterCoreSmokeTests(unittest.TestCase):
    def test_cycle_is_safe_and_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = MasterCore.__new__(MasterCore)
            core.root = tmp
            core.data_dir = os.path.join(tmp, "data")
            core.sandbox_dir = os.path.join(tmp, "sandbox", "autonomous_workspace")
            core.state_file = os.path.join(core.data_dir, "master_core_state.json")
            core.access_manager = AccessManager(tmp)
            os.makedirs(core.data_dir, exist_ok=True)
            os.makedirs(core.sandbox_dir, exist_ok=True)
            core.state = {
                "version": core.VERSION,
                "cycles": 0,
                "agents": [],
                "capabilities": [],
                "proposals": [],
                "access_requests": [],
                "last_cycle": None,
            }

            result = core.run_cycle()

            self.assertEqual(result["cycle"], 1)
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_changes_allowed"])
            self.assertTrue(result["sandbox_only"])
            self.assertIn("capabilities", result)
            self.assertIn("proposals", result)
            self.assertIn("access_requirements", result)

    def test_proposals_are_replaced_not_accumulated(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = MasterCore.__new__(MasterCore)
            core.root = tmp
            core.data_dir = tmp
            core.sandbox_dir = tmp
            core.state_file = os.path.join(tmp, "state.json")
            core.state = {
                "version": core.VERSION,
                "cycles": 0,
                "agents": [],
                "capabilities": [],
                "proposals": [{"old": True}],
                "access_requests": [],
                "last_cycle": None,
            }

            proposals = core.create_proposals(["planning"], [])

            self.assertEqual(len(proposals), 1)
            self.assertEqual(core.state["proposals"], proposals)
            self.assertFalse(any(item.get("old") for item in proposals))


if __name__ == "__main__":
    unittest.main()
