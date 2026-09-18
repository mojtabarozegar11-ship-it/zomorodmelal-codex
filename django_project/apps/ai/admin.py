from django import forms
from django.contrib import admin
from .models import AIConfiguration


class AIConfigurationAdminForm(forms.ModelForm):
    api_key = forms.CharField(
        required=False,
        label="API key",
        widget=forms.PasswordInput(
            render_value=False,
            attrs={"autocomplete": "new-password"},
        ),
        help_text="Leave blank to keep the existing key. The stored key is never shown.",
    )

    class Meta:
        model = AIConfiguration
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Never expose an existing secret through the form's initial state.
        self.initial["api_key"] = None

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_key = self.cleaned_data.get("api_key", "").strip()
        if new_key:
            instance.api_key = new_key
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    form = AIConfigurationAdminForm
    list_display = ("provider", "enabled", "model", "has_api_key", "updated_at")
    list_filter = ("provider", "enabled")
    search_fields = ("provider", "model")
    readonly_fields = ("updated_at", "has_api_key")
    fields = (
        "provider",
        "enabled",
        "api_key",
        "base_url",
        "model",
        "has_api_key",
        "updated_at",
    )

    @admin.display(boolean=True, description="API key configured")
    def has_api_key(self, obj):
        return bool(obj.api_key)

from .content_agent_models import ContentChannel, ContentCompetitor, ContentStrategy, ContentResearchSnapshot, ContentBrief, ContentAsset, ContentPublication, ContentPerformance

admin.site.register(ContentChannel, ContentChannelAdmin)
admin.site.register(ContentCompetitor, ContentCompetitorAdmin)
admin.site.register(ContentStrategy, ContentStrategyAdmin)
admin.site.register(ContentResearchSnapshot, ContentResearchSnapshotAdmin)
admin.site.register(ContentBrief, ContentBriefAdmin)
admin.site.register(ContentAsset, ContentAssetAdmin)
admin.site.register(ContentPublication, ContentPublicationAdmin)
admin.site.register(ContentPerformance, ContentPerformanceAdmin)

from .content_agent_models import ContentExperiment

@admin.register(ContentExperiment)
class ContentExperimentAdmin(admin.ModelAdmin):
    list_display = ("name", "publication", "variant", "active", "created_at")
    list_filter = ("active", "variant")
    search_fields = ("name", "hypothesis")
