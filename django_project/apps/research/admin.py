from django.contrib import admin

from .models import ResearchProject


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "owner_approval_required", "owner_approved", "updated_at")
    list_filter = ("status", "owner_approval_required", "owner_approved")
    search_fields = ("title", "summary")
    readonly_fields = ("created_at", "updated_at")
