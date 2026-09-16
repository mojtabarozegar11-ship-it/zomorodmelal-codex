import tempfile
import unittest
from pathlib import Path

from autonomous_core.change_package import ChangePackage
from controller.deployment_gate import DeploymentGate


class DeploymentGateTests(unittest.TestCase):
    def test_prepare_creates_owner_approval_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = ChangePackage(root / "data" / "change_packages").create(
                [{"path": "app.py", "sha256": "a" * 64, "size": 1}],
                "verified sandbox change",
                "sandbox",
            )
            gate = DeploymentGate(root)
            result = gate.prepare(package["package_id"], "promote verified change")
            self.assertEqual(result["status"], "waiting_approval")
            self.assertTrue(result["owner_approval_required"])

    def test_deploy_is_blocked_without_owner_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = ChangePackage(root / "data" / "change_packages").create(
                [{"path": "app.py", "sha256": "a" * 64, "size": 1}],
                "verified sandbox change",
                "sandbox",
            )
            gate = DeploymentGate(root)
            result = gate.deploy(package["package_id"], 999)
            self.assertEqual(result["status"], "approval_required")
            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
