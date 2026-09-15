import hashlib
import tempfile
import unittest
from pathlib import Path

from autonomous_core.change_package import ChangePackage
from controller.change_package_executor import ChangePackageExecutor


class ChangePackageExecutorTests(unittest.TestCase):
    def _package_and_request(self, root, text="approved content"):
        sandbox = root / "data" / "sandbox" / "cycle_1"
        sandbox.mkdir(parents=True)
        source = sandbox / "demo.txt"
        source.write_text(text, encoding="utf-8")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        package = ChangePackage(root / "data" / "change_packages").create(
            [{"path": "demo.txt", "sha256": digest, "size": source.stat().st_size}],
            "executor test",
            sandbox_rel="data/sandbox/cycle_1",
        )
        executor = ChangePackageExecutor(root)
        request = executor.approval.request(
            "change_package_deploy",
            "test promotion",
            metadata={"package_id": package["package_id"], "package_sha256": package["package_sha256"]},
        )
        return executor, package, request

    def test_promotes_only_after_owner_approval_and_hash_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executor, package, request = self._package_and_request(root)
            blocked = executor.execute(package["package_id"], request["id"])
            self.assertEqual(blocked["status"], "approval_required")

            executor.approval.approve(request["id"])
            result = executor.execute(package["package_id"], request["id"])
            self.assertTrue(result["success"])
            self.assertEqual(result["status"], "promoted")
            self.assertEqual((root / "demo.txt").read_text(encoding="utf-8"), "approved content")
            self.assertFalse((root / "demo.txt.master-agent.tmp").exists())

    def test_replay_of_same_approved_request_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executor, package, request = self._package_and_request(root)
            executor.approval.approve(request["id"])
            first = executor.execute(package["package_id"], request["id"])
            second = executor.execute(package["package_id"], request["id"])
            self.assertTrue(first["success"])
            self.assertEqual(second["status"], "already_executed")

    def test_rejects_tampered_sandbox_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executor, package, request = self._package_and_request(root, "original")
            executor.approval.approve(request["id"])
            (root / "data" / "sandbox" / "cycle_1" / "demo.txt").write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                executor.execute(package["package_id"], request["id"])
            self.assertFalse((root / "demo.txt").exists())


if __name__ == "__main__":
    unittest.main()
