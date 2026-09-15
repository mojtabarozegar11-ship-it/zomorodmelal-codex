import os
import tempfile
import unittest
from pathlib import Path

from autonomous_core.autonomous_cycle import AutonomousCycle


class AutonomousCycleGoalTests(unittest.TestCase):
    @unittest.skipIf(os.getenv("AUTONOMOUS_CYCLE_INNER_TESTS") == "1", "outer autonomous-cycle test")
    def test_website_goal_creates_approval_bound_site_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = AutonomousCycle(root).run("ساخت و توسعه سایت شرکت")

            self.assertEqual(result["report"]["goal"], "ساخت و توسعه سایت شرکت")
            self.assertTrue(result["tests"]["passed"])
            self.assertIsNotNone(result["package"])
            self.assertIsNotNone(result["approval_request"])
            self.assertTrue(result["safety"]["owner_approval_required"])
            self.assertFalse(result["safety"]["real_deployment"])

            sandbox = root / "data" / "sandbox" / "cycle_1" / "site"
            self.assertTrue((sandbox / "index.html").is_file())
            self.assertTrue((sandbox / "styles.css").is_file())
            self.assertTrue((sandbox / "app.js").is_file())

            metadata = result["approval_request"]["metadata"]
            self.assertEqual(metadata["goal"], "ساخت و توسعه سایت شرکت")
            self.assertEqual(metadata["package_id"], result["package"]["package_id"])


if __name__ == "__main__":
    unittest.main()
