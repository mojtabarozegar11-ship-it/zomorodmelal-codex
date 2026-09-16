import tempfile
import unittest

from autonomous_core.access_manager import AccessManager
from autonomous_core.activation_gate import ActivationGate


class ActivationGateTests(unittest.TestCase):
    def test_only_approved_matching_request_gets_authorization(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(tmp)
            request = manager.request("github_repo", "update company site", "repository:main")
            gate = ActivationGate(tmp, manager)

            with self.assertRaises(PermissionError):
                gate.authorize(request["request_id"], "github_repo", "repository:main")

            manager.approve(request["request_id"])
            decision = gate.authorize(request["request_id"], "github_repo", "repository:main")
            self.assertTrue(decision["authorized"])
            self.assertFalse(decision["credentials_acquired"])
            self.assertFalse(decision["activated"])
            self.assertFalse(decision["external_action_allowed"])

    def test_capability_and_scope_must_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(tmp)
            request = manager.request("github_repo", "update", "repository:main")
            manager.approve(request["request_id"])
            gate = ActivationGate(tmp, manager)

            with self.assertRaises(PermissionError):
                gate.authorize(request["request_id"], "hosting", "repository:main")
            with self.assertRaises(PermissionError):
                gate.authorize(request["request_id"], "github_repo", "repository:other")

    def test_revoked_request_cannot_be_authorized(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(tmp)
            request = manager.request("hosting", "deploy", "site:production")
            manager.approve(request["request_id"])
            manager.revoke(request["request_id"])
            gate = ActivationGate(tmp, manager)

            with self.assertRaises(PermissionError):
                gate.authorize(request["request_id"], "hosting", "site:production")


if __name__ == "__main__":
    unittest.main()
