import unittest
from django.test import Client


class SecurityHeadersTests(SimpleTestCase):
    def test_security_headers_are_enabled(self):
        response = Client().get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertIn("Referrer-Policy", response)
