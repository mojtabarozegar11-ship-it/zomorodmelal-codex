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


if __name__ == "__main__":
    unittest.main()
