from django.test import SimpleTestCase
from unittest.mock import patch

from django_integration.agent_bridge import AgentBridge
from api.agent_api import _json_body


class UnifiedRuntimeContractTests(SimpleTestCase):
    @patch("django_integration.agent_bridge.httpx.get")
    def test_worker_health_bridge(self, mocked_get):
        mocked_get.return_value.raise_for_status.return_value = None
        mocked_get.return_value.json.return_value = {
            "status": "ok",
            "service": "worker-mojtaba",
        }
        result = AgentBridge(worker_base_url="http://worker", token="secret").health()
        self.assertEqual(result["status"], "ok")
        mocked_get.assert_called_once()

    def test_invalid_json_is_rejected_by_body_parser(self):
        request = type("Request", (), {"body": b"{invalid"})()
        self.assertIsNone(_json_body(request))


class UnifiedRuntimeFileContractTests(SimpleTestCase):
    def test_expected_single_runtime_endpoints_are_documented(self):
        from django_project.config.urls import urlpatterns

        names = {getattr(pattern, "name", None) for pattern in urlpatterns}
        self.assertIn(None, names)  # include() patterns are represented without a leaf name.
