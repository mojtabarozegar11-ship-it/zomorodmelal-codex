import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()

from django.test import TestCase, override_settings
from django.contrib.admin.sites import AdminSite

from apps.ai.admin import AIConfigurationAdmin, AIConfigurationAdminForm
from apps.ai.models import AIConfiguration
from apps.ai.services import get_deepseek_provider


class AIAdminConfigurationTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AIConfigurationAdmin(AIConfiguration, self.site)

    def test_existing_key_is_not_rendered_as_initial_value(self):
        item = AIConfiguration.objects.create(provider="deepseek", api_key="secret-value")
        form = AIConfigurationAdminForm(instance=item)
        self.assertFalse(form.initial.get("api_key"))

    def test_blank_key_preserves_existing_key(self):
        item = AIConfiguration.objects.create(provider="deepseek", api_key="secret-value")
        form = AIConfigurationAdminForm(
            data={
                "provider": "deepseek",
                "enabled": "",
                "api_key": "",
                "base_url": "https://api.deepseek.com",
                "model": "deepseek-chat",
            },
            instance=item,
        )
        self.assertTrue(form.is_valid(), form.errors)
        saved = form.save()
        self.assertEqual(saved.api_key, "secret-value")

    @override_settings(AI_PROVIDER_ENABLED=False)
    def test_external_ai_disabled(self):
        self.assertIsNone(get_deepseek_provider())

    @override_settings(AI_PROVIDER_ENABLED=True)
    def test_enabled_deepseek_configuration_builds_provider(self):
        AIConfiguration.objects.create(
            provider="deepseek",
            enabled=True,
            api_key="secret-value",
            base_url="https://api.deepseek.com",
        )
        provider = get_deepseek_provider()
        self.assertIsNotNone(provider)
        self.assertEqual(provider.model, "deepseek-chat")
