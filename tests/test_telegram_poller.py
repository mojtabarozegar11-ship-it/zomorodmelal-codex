import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from approval.telegram_poller import TelegramApprovalPoller


class TelegramPollerTests(unittest.TestCase):
    def test_poll_once_processes_callback_and_persists_offset(self):
        with tempfile.TemporaryDirectory() as tmp:
            poller = TelegramApprovalPoller(tmp)
            poller.telegram.token = "token"
            poller.telegram.owner_chat_id = "123"
            callback_data = poller.telegram.build_callback(1, "approve")
            with patch.object(poller.telegram, "_call", return_value={
                "ok": True,
                "result": [{
                    "update_id": 41,
                    "callback_query": {
                        "id": "cb-1",
                        "data": callback_data,
                        "message": {"chat": {"id": "123"}},
                    },
                }],
            }), patch.object(poller.telegram, "handle_callback", return_value={"success": True, "status": "approved"}), patch.object(poller.telegram, "answer_callback") as answer:
                result = poller.poll_once()
            self.assertEqual(result["processed"], 1)
            self.assertEqual(result["next_offset"], 42)
            answer.assert_called_once_with("cb-1", "approved")
            self.assertIn('"offset": 42', poller.offset_path.read_text(encoding="utf-8"))

    def test_disabled_poller_does_not_call_telegram(self):
        with tempfile.TemporaryDirectory() as tmp:
            poller = TelegramApprovalPoller(tmp)
            with patch.object(poller.telegram, "_call") as call:
                result = poller.poll_once()
            self.assertEqual(result["status"], "disabled")
            call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
