from importlib import import_module

from django.apps import AppConfig


class AIConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai"
    verbose_name = "AI"

    def ready(self):
        import_module("apps.ai.content_agent_models")
        import_module("apps.ai.content_agent_admin")
