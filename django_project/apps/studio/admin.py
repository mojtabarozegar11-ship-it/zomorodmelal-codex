from django.contrib import admin
from .models import StudioIdea, StudioMilestone, StudioProject


@admin.register(StudioProject)
class StudioProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "status", "nft_enabled", "real_release_approved", "updated_at")
    list_filter = ("kind", "status", "nft_enabled", "real_release_approved")
    search_fields = ("name", "slug", "concept")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(StudioIdea)
class StudioIdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "explored", "approved_for_prototyping", "created_at")
    list_filter = ("explored", "approved_for_prototyping")
    search_fields = ("title", "description")


@admin.register(StudioMilestone)
class StudioMilestoneAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "done", "created_at")
    list_filter = ("done",)
    search_fields = ("title", "project__name")
