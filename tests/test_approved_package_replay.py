import hashlib
import tempfile
import unittest
from pathlib import Path

from autonomous_core.change_package import ChangePackage
from controller.change_package_executor import ChangePackageExecutor


class ApprovedPackageReplayTests(unittest.TestCase):
    def test_same_approved_request_cannot_promote_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sandbox = root / "data" / "sandbox" / "cycle_1"
            sandbox.mkdir(parents=True)
            source = sandbox / "demo.txt"
            source.write_text("v1", encoding="utf-8")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            package = ChangePackage(root / "data" / "change_packages").create(
                [{"path": "demo.txt", "sha256": digest, "size": source.stat().st_size}],
                "replay protection",
                sandbox_rel="data/sandbox/cycle_1",
            )
            executor = ChangePackageExecutor(root)
            request = executor.approval.request(
                "change_package_deploy",
                "replay protection",
                metadata={
                    "package_id": package["package_id"],
                    "package_sha256": package["package_sha256"],
                },
            )
            executor.approval.approve(request["id"])
            first = executor.execute(package["package_id"], request["id"])
            self.assertTrue(first["success"])
            second = executor.execute(package["package_id"], request["id"])
            self.assertTrue(second["success"])
            self.assertEqual((root / "demo.txt").read_text(encoding="utf-8"), "v1")

    def test_package_binding_mismatch_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sandbox = root / "data" / "sandbox" / "cycle_2"
            sandbox.mkdir(parents=True)
            source = sandbox / "demo.txt"
            source.write_text("safe", encoding="utf-8")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            package = ChangePackage(root / "data" / "change_packages").create(
                [{"path": "demo.txt", "sha256": digest, "size": source.stat().st_size}],
                "binding protection",
                sandbox_rel="data/sandbox/cycle_2",
            )
            executor = ChangePackageExecutor(root)
            request = executor.approval.request(
                "change_package_deploy",
                "binding protection",
                metadata={"package_id": "wrong", "package_sha256": package["package_sha256"]},
            )
            executor.approval.approve(request["id"])
            result = executor.execute(package["package_id"], request["id"])
            self.assertEqual(result["status"], "package_binding_mismatch")
            self.assertFalse((root / "demo.txt").exists())


if __name__ == "__main__":
    unittest.main()
