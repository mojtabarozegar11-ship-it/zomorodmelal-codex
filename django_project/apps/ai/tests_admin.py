import os
import sys
import django
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.admin.sites import AdminSite

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()

from apps.ai.admin import AIConfigurationAdmin
from apps.ai.models import AIConfiguration
from apps.ai.services import get_deepseek_provider


class AIAdminConfigurationTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = AIConfigurationAdmin(AIConfiguration, self.site)

    def test_admin_form_accepts_key_without_rendering_existing_value(self):
        from apps.ai.admin import AIConfigurationAdminForm
        item = AIConfiguration.objects.create(provider="deepseek", api_key="secret-value")
        form = AIConfigurationAdminForm(instance=item)
        self.assertEqual(form.initial["api_key"], None)

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
