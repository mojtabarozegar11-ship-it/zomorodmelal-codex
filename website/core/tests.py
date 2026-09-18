from django.test import SimpleTestCase
from django.urls import resolve


class WebsiteContractTests(SimpleTestCase):
    def test_home_route(self):
        self.assertEqual(resolve("/").url_name, "home")

    def test_health_route(self):
        self.assertEqual(resolve("/health/").url_name, "website-health")

    def test_page_route(self):
        self.assertEqual(resolve("/page/example/").url_name, "page-detail")
