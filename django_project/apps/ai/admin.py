from django.contrib import admin
from .models import AIConfiguration


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = ("provider","enabled","model","updated_at")
    list_filter = ("provider","enabled")
    search_fields = ("provider","model")
    readonly_fields = ("updated_at",)
    exclude = ("api_key",)
