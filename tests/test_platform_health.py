import os
import unittest

from django.conf import settings


class ProductionConfigTests(unittest.TestCase):
    def test_settings_have_production_paths(self):
        self.assertEqual(settings.MEDIA_URL, "/media/")
        self.assertTrue(str(settings.MEDIA_ROOT))
        self.assertTrue(str(settings.STATIC_ROOT))

    def test_ai_keys_are_environment_only(self):
        self.assertFalse(hasattr(settings, "DEEPSEEK_API_KEY"))
        self.assertFalse(hasattr(settings, "OPENAI_API_KEY"))


class PlatformHealthTests(unittest.TestCase):
    def test_canonical_provider_adapter(self):
        from ai_engine.legacy_adapter import provider_status
        status = provider_status("deepseek")
        self.assertEqual(status["provider"], "deepseek")

    def test_tool_registry(self):
        from master_agent import ToolRegistry
        tools = ToolRegistry()
        tools.register("noop", lambda x: x)
        self.assertIn("noop", tools.names())


if __name__ == "__main__":
    unittest.main()
