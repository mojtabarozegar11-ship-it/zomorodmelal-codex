from django.contrib import admin
from .models import SitePage, ActivityLog

@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display=("title","slug","published")
    list_filter=("published",)
    search_fields=("title","slug","content")
    prepopulated_fields={"slug":("title",)}

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display=("action","created_at")
    search_fields=("action",)
    readonly_fields=("created_at",)
