"""End-to-end tests for the single Site -> Master -> Worker runtime."""
from __future__ import annotations

from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from api.agent_api import agent_status, execute_goal
from django.http import HttpRequest
from django_integration.agent_bridge import AgentBridge


def request(method="GET", body=b""):
    req = HttpRequest()
    req.method = method
    req._body = body
    return req


class UnifiedRuntimeTests(SimpleTestCase):
    def test_status_exposes_single_runtime(self):
        response = agent_status(request())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"site -> master -> worker -> execution -> result", response.content)

    def test_execute_requires_post(self):
        response = execute_goal(request())
        self.assertEqual(response.status_code, 405)

    def test_execute_rejects_invalid_json(self):
        response = execute_goal(request("POST", b"{invalid"))
        self.assertEqual(response.status_code, 400)

    def test_execute_requires_goal(self):
        response = execute_goal(request("POST", b"{}"))
        self.assertEqual(response.status_code, 400)

    @override_settings(ROOT_URLCONF="config.urls")
    @patch.object(AgentBridge, "execute_goal")
    def test_execute_delegates_to_worker_bridge(self, mocked_execute):
        mocked_execute.return_value = {
            "status": "approval_required",
            "goal": "تست یکپارچه",
            "plan": ["analyze", "execute", "validate", "report"],
        }
        response = execute_goal(
            request(
                "POST",
                b'{"goal":"\u062a\u0633\u062a \u06cc\u06a9\u067e\u0627\u0631\u0686\u0647","context":{"source":"site"}}',
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"approval_required", response.content)
        mocked_execute.assert_called_once_with(
            "تست یکپارچه", context={"source": "site"}, approved=False
        )
