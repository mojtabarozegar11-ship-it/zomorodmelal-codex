import asyncio
import unittest
from unittest.mock import AsyncMock

import main


class FakeUser:
    def __init__(self, user_id):
        self.id = user_id


class FakeUpdate:
    def __init__(self, user_id, callback_data):
        self.effective_user = FakeUser(user_id)
        self.callback_query = type("Query", (), {})()
        self.callback_query.from_user = FakeUser(user_id)
        self.callback_query.data = callback_data
        self.callback_query.answer = AsyncMock()
        self.callback_query.edit_message_text = AsyncMock()


class FakeAccessManager:
    def __init__(self):
        self.calls = []

    def approve(self, request_id):
        self.calls.append(("approve", request_id))
        return {
            "request_id": request_id,
            "capability": "web_research",
            "resource": "internet_research",
            "risk_level": "low",
            "access_level": "read",
            "goal": "research market",
            "scope": "minimum_required",
            "status": "approved_pending_activation",
            "credentials_acquired": False,
            "activated": False,
        }

    def revoke(self, request_id):
        self.calls.append(("revoke", request_id))
        return {
            "request_id": request_id,
            "capability": "web_research",
            "resource": "internet_research",
            "risk_level": "low",
            "access_level": "read",
            "goal": "research market",
            "scope": "minimum_required",
            "status": "revoked",
            "credentials_acquired": False,
            "activated": False,
        }


class TelegramSecurityTests(unittest.TestCase):
    def test_owner_check_rejects_non_owner(self):
        old_owner = main.OWNER_ID
        try:
            main.OWNER_ID = 12345
            update = type("Update", (), {"effective_user": FakeUser(99999)})()
            self.assertFalse(main.is_owner(update))
        finally:
            main.OWNER_ID = old_owner

    def test_access_callback_rejects_non_owner_before_access_manager(self):
        old_owner = main.OWNER_ID
        try:
            main.OWNER_ID = 12345
            update = FakeUpdate(99999, "access:approve:1")
            asyncio.run(main.access_callback(update, None))
            update.callback_query.answer.assert_awaited_once()
            update.callback_query.edit_message_text.assert_not_awaited()
        finally:
            main.OWNER_ID = old_owner

    def test_access_callback_rejects_malformed_request_for_owner(self):
        old_owner = main.OWNER_ID
        try:
            main.OWNER_ID = 12345
            update = FakeUpdate(12345, "access:approve")
            asyncio.run(main.access_callback(update, None))
            update.callback_query.answer.assert_awaited_once()
            update.callback_query.edit_message_text.assert_awaited_once_with(
                "❌ درخواست دسترسی نامعتبر است."
            )
        finally:
            main.OWNER_ID = old_owner

    def test_access_callback_approval_does_not_activate_credentials(self):
        old_owner = main.OWNER_ID
        old_manager = main.access_manager
        try:
            main.OWNER_ID = 12345
            main.access_manager = FakeAccessManager()
            update = FakeUpdate(12345, "access:approve:req-1")
            asyncio.run(main.access_callback(update, None))
            update.callback_query.edit_message_text.assert_awaited_once()
            message = update.callback_query.edit_message_text.await_args.args[0]
            self.assertIn("اعتبارنامه هنوز فعال نشده است", message)
            self.assertIn("اعتبارنامه فعال: خیر", message)
            self.assertEqual(main.access_manager.calls, [("approve", "req-1")])
        finally:
            main.access_manager = old_manager
            main.OWNER_ID = old_owner

    def test_access_callback_revoke_reports_no_active_credentials(self):
        old_owner = main.OWNER_ID
        old_manager = main.access_manager
        try:
            main.OWNER_ID = 12345
            main.access_manager = FakeAccessManager()
            update = FakeUpdate(12345, "access:revoke:req-2")
            asyncio.run(main.access_callback(update, None))
            update.callback_query.edit_message_text.assert_awaited_once()
            message = update.callback_query.edit_message_text.await_args.args[0]
            self.assertIn("هیچ اعتبارنامه‌ای فعال نشد", message)
            self.assertIn("اعتبارنامه فعال: خیر", message)
            self.assertEqual(main.access_manager.calls, [("revoke", "req-2")])
        finally:
            main.access_manager = old_manager
            main.OWNER_ID = old_owner


if __name__ == "__main__":
    unittest.main()
