import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from approval.approval_gateway import ApprovalGateway
from approval.telegram_approval import TelegramApproval


class TelegramApprovalTests(unittest.TestCase):
    def test_disabled_without_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = TelegramApproval(tmp, token="", owner_chat_id="")
            self.assertFalse(bot.enabled)
            self.assertEqual(bot.notify({"id": 1})["status"], "disabled")

    def test_callback_requires_owner_chat(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = TelegramApproval(tmp, token="token", owner_chat_id="123")
            data = bot.build_callback(1, "approve")
            result = bot.handle_callback({"data": data, "message": {"chat": {"id": 999}}})
            self.assertEqual(result["status"], "unauthorized")

    def test_callback_requires_valid_token_and_approves(self):
        with tempfile.TemporaryDirectory() as tmp:
            gateway = ApprovalGateway(tmp)
            request = gateway.request("deploy", "test")
            with patch.dict(os.environ, {}, clear=True):
                bot = TelegramApproval(tmp, token="token", owner_chat_id="123")
                data = bot.build_callback(request["id"], "approve")
                result = bot.handle_callback({"data": data, "message": {"chat": {"id": "123"}}})
            self.assertTrue(result["success"])
            self.assertEqual(result["status"], "approved")
            self.assertTrue(gateway.is_approved(request["id"]))

    def test_tampered_callback_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            gateway = ApprovalGateway(tmp)
            request = gateway.request("deploy", "test")
            bot = TelegramApproval(tmp, token="token", owner_chat_id="123")
            data = bot.build_callback(request["id"], "approve")[:-1] + "0"
            result = bot.handle_callback({"data": data, "message": {"chat": {"id": "123"}}})
            self.assertEqual(result["status"], "invalid_token")
            self.assertFalse(gateway.is_approved(request["id"]))


if __name__ == "__main__":
    unittest.main()
