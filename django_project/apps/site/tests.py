from django.test import SimpleTestCase
from django.urls import resolve

class SiteContractTests(SimpleTestCase):
    def test_routes(self):
        self.assertEqual(resolve("/").url_name, "home")
        self.assertEqual(resolve("/health/").url_name, "website-health")
        self.assertEqual(resolve("/encyclopedia/").url_name, "encyclopedia")
        self.assertEqual(resolve("/page/example/").url_name, "page-detail")
