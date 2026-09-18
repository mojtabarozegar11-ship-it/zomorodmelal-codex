import unittest
from django.test import Client, TestCase


class PrimarySiteE2E(TestCase):
    def test_public_and_management_routes(self):
        client=Client()
        paths=["/","/services/","/encyclopedia/","/economy/","/studio/","/health/","/mobile-admin/","/api/status/"]
        for path in paths:
            response=client.get(path)
            self.assertIn(response.status_code,(200,301,302,401,403,404),msg=path)

    def test_brand_template_present(self):
        response=Client().get("/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"زمرد ملل")
