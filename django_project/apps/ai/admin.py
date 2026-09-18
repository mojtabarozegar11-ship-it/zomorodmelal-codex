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
        self._existing_api_key = self.instance.api_key
        self.initial["api_key"] = None

    def save(self, commit=True):
        existing_key = self._existing_api_key
        instance = super().save(commit=False)
        new_key = self.cleaned_data.get("api_key", "").strip()
        instance.api_key = new_key or existing_key
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
