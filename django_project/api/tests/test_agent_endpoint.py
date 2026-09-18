import json
import os
import sys

import django
from django.test import TestCase, Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()


class AgentEndpointTests(TestCase):
    def test_status(self):
        response=Client().get("/api/status/")
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.json()["owner_approval_required"])

    def test_execute_requires_goal(self):
        response=Client().post("/api/execute/", data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code,400)
