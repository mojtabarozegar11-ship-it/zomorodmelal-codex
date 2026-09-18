import unittest
from django.test import Client


class ProductionSecuritySmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_security_headers_and_health(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Content-Type-Options", response)
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
