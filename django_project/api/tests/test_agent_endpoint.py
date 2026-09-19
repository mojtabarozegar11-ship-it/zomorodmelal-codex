import json
import os
import sys

import django
from django.test import Client, TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()


class AgentEndpointTests(TestCase):
    def test_status(self):
        response = Client().get("/api/status/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["owner_approval_required"])
        self.assertEqual(payload["status"], "ready")

    def test_execute_requires_goal(self):
        response = Client().post(
            "/api/execute/",
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_execute_returns_approval_request(self):
        response = Client().post(
            "/api/execute/",
            data=json.dumps({"goal": "اجرای آزمایشی"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["goal"], "اجرای آزمایشی")
        self.assertTrue(payload["waiting_for_approval"])
