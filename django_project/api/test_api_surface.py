import unittest
from django.test import Client


class ApiSurfaceSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_status_endpoint(self):
        response = self.client.get("/api/status/")
        self.assertIn(response.status_code, (200, 401, 403))

    def test_execute_endpoint_is_protected_or_reachable(self):
        response = self.client.post("/api/execute/", data={})
        self.assertIn(response.status_code, (200, 400, 401, 403, 405))
