import tempfile
import unittest
from pathlib import Path

from autonomous_core.change_package import ChangePackage


class ChangePackageTests(unittest.TestCase):
    def test_creates_approval_gated_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = ChangePackage(Path(tmp) / "packages")
            result = package.create(
                [{"path": "demo.py", "sha256": "abc", "size": 3}],
                "safe builder verification",
            )
            self.assertEqual(result["status"], "awaiting_owner_approval")
            self.assertTrue(result["owner_approval_required"])
            self.assertFalse(result["real_changes_allowed"])
            self.assertEqual(package.get(result["package_id"])["package_sha256"], result["package_sha256"])


if __name__ == "__main__":
    unittest.main()
