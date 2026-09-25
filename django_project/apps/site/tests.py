from django.contrib.staticfiles.finders import find
from django.test import SimpleTestCase
from django.urls import resolve, reverse


class SiteContractTests(SimpleTestCase):
    def test_routes(self):
        self.assertEqual(resolve("/").url_name, "home")
        self.assertEqual(resolve("/health/").url_name, "website-health")
        self.assertEqual(resolve("/encyclopedia/").url_name, "encyclopedia")
        self.assertEqual(resolve("/games/").url_name, "games")
        self.assertEqual(resolve("/page/example/").url_name, "page-detail")

    def test_core_site_assets_exist(self):
        for asset in (
            "site/logo.svg",
            "site/main.css",
            "site/design-tokens.css",
            "site/components.css",
        ):
            with self.subTest(asset=asset):
                self.assertIsNotNone(find(asset), asset)

    def test_home_renders_foundation_contract(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="main-content"')
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'site/main.css')
        self.assertContains(response, 'site/logo.svg')
        self.assertContains(response, "چهار دروازه اصلی")
        self.assertContains(response, "ورود سریع به بخش‌ها")
