import tempfile
import unittest
from pathlib import Path

from autonomous_core.access_manager import AccessManager


class AccessManagerTests(unittest.TestCase):
    def test_discover_is_metadata_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            result = manager.discover(["web_research", "hosting", "unknown"])
            self.assertEqual([x["capability"] for x in result], ["hosting", "web_research"])
            self.assertTrue(all(x["owner_approval_required"] for x in result))
            self.assertTrue(all(not x["credentials_acquired"] for x in result))
            self.assertTrue(all(not x["activated"] for x in result))

    def test_request_requires_owner_approval_and_never_activates(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            request = manager.request("github_repo", "update company site")
            self.assertEqual(request["status"], "waiting_owner_approval")
            self.assertTrue(request["owner_approval_required"])
            self.assertFalse(request["credentials_acquired"])
            self.assertFalse(request["activated"])

            approved = manager.approve(request["request_id"])
            self.assertEqual(approved["status"], "approved_pending_activation")
            self.assertFalse(approved["credentials_acquired"])
            self.assertFalse(approved["activated"])

    def test_revoke_disables_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            request = manager.request("hosting", "deploy approved site")
            revoked = manager.revoke(request["request_id"])
            self.assertEqual(revoked["status"], "revoked")
            self.assertFalse(revoked["activated"])

    def test_unknown_capability_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = AccessManager(Path(tmp))
            with self.assertRaises(ValueError):
                manager.request("not_real", "test")


if __name__ == "__main__":
    unittest.main()
