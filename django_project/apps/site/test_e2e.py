import unittest
from django.test import Client


class SiteE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_core_pages_are_reachable(self):
        for path in ["/", "/encyclopedia/", "/health/", "/games/"]:
            response = self.client.get(path)
            self.assertIn(response.status_code, (200, 301, 302), path)
