from django.test import SimpleTestCase
from django.conf import settings


class SecurityFoundationTests(SimpleTestCase):
    def test_https_proxy_and_host_contract(self):
        self.assertEqual(settings.SECURE_PROXY_SSL_HEADER, ("HTTP_X_FORWARDED_PROTO", "https"))
        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertIn("zomorodmelal.ir", settings.ALLOWED_HOSTS)
        self.assertIn("www.zomorodmelal.ir", settings.ALLOWED_HOSTS)
        self.assertIn("https://zomorodmelal.ir", settings.CSRF_TRUSTED_ORIGINS)
        self.assertIn("https://www.zomorodmelal.ir", settings.CSRF_TRUSTED_ORIGINS)

    def test_secure_cookies_are_enabled_when_debug_is_false(self):
        self.assertFalse(settings.DEBUG)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)

    def test_production_real_execution_remains_disabled_by_default(self):
        self.assertFalse(settings.ECONOMIC_REAL_EXECUTION_ENABLED)
