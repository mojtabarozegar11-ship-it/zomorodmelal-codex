import json
from django.test import Client, SimpleTestCase


class AgentApiCanonicalTests(SimpleTestCase):
    def test_status_uses_canonical_engine(self):
        response=Client().get("/api/status/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()["engine"],"master_agent")

    def test_execution_requires_owner_approval(self):
        response=Client().post("/api/execute/",data=json.dumps({"goal":"publish"}),content_type="application/json")
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.json()["status"],"approval_required")

    def test_invalid_json_is_rejected(self):
        response=Client().post("/api/execute/",data="{",content_type="application/json")
        self.assertEqual(response.status_code,400)
