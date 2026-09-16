import tempfile
import unittest
from pathlib import Path

from autonomous_core.access_manager import AccessManager
from autonomous_core.master_core import MasterCore


class GoalAccessRequirementTests(unittest.TestCase):
    def test_access_manager_catalog_is_not_activated_by_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            requirements = manager.discover(["web_research", "github_repo"])
            self.assertEqual([x["capability"] for x in requirements], ["github_repo", "web_research"])
            self.assertTrue(all(x["owner_approval_required"] for x in requirements))
            self.assertTrue(all(not x["credentials_acquired"] for x in requirements))
            self.assertTrue(all(not x["activated"] for x in requirements))

    def test_request_is_idempotent_for_same_goal(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            first = manager.request("hosting", "publish approved site")
            second = manager.request("hosting", "publish approved site")
            self.assertEqual(first["request_id"], second["request_id"])
            self.assertEqual(manager.status()["total"], 1)
            self.assertEqual(manager.status()["credentials_acquired"], 0)
            self.assertEqual(manager.status()["activated"], 0)

    def test_master_core_preserves_access_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            core = MasterCore(Path(tmp))
            core.set_goal("research and develop the company website")
            requirements = core.discover_access_requirements()
            self.assertTrue(all(x["owner_approval_required"] for x in requirements))
            self.assertTrue(all(not x["credentials_acquired"] for x in requirements))
            self.assertTrue(all(not x["activated"] for x in requirements))


if __name__ == "__main__":
    unittest.main()
