from django.contrib import admin

from .content_agent_models import (
    ContentAsset,
    ContentBrief,
    ContentChannel,
    ContentCompetitor,
    ContentPerformance,
    ContentPublication,
    ContentResearchSnapshot,
    ContentStrategy,
)


@admin.register(ContentChannel)
class ContentChannelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "platform",
        "topic",
        "active",
        "auto_publish",
        "owner_approved",
        "updated_at",
    )
    list_filter = ("platform", "active", "auto_publish", "owner_approved")
    search_fields = ("name", "handle", "topic")


@admin.register(ContentCompetitor)
class ContentCompetitorAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "channel", "active")
    list_filter = ("platform", "active")
    search_fields = ("name", "url", "channel__name")


@admin.register(ContentStrategy)
class ContentStrategyAdmin(admin.ModelAdmin):
    list_display = ("channel", "active", "updated_at")
    list_filter = ("active",)
    search_fields = ("channel__name",)


@admin.register(ContentResearchSnapshot)
class ContentResearchSnapshotAdmin(admin.ModelAdmin):
    list_display = ("query", "source", "channel", "captured_at")
    list_filter = ("source",)
    search_fields = ("query", "title", "url", "channel__name")
    readonly_fields = ("captured_at",)


@admin.register(ContentBrief)
class ContentBriefAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "channel",
        "format",
        "status",
        "owner_approved",
        "created_at",
    )
    list_filter = ("status", "format", "owner_approved")
    search_fields = ("topic", "angle", "channel__name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContentAsset)
class ContentAssetAdmin(admin.ModelAdmin):
    list_display = ("brief", "asset_type", "version", "approved", "created_at")
    list_filter = ("asset_type", "approved")
    search_fields = ("body", "brief__topic")
    readonly_fields = ("created_at",)


@admin.register(ContentPublication)
class ContentPublicationAdmin(admin.ModelAdmin):
    list_display = (
        "brief",
        "channel",
        "status",
        "provider",
        "owner_approved",
        "scheduled_for",
        "published_at",
    )
    list_filter = ("status", "provider", "owner_approved")
    search_fields = ("external_id", "idempotency_key", "brief__topic")
    readonly_fields = ("created_at", "published_at")


@admin.register(ContentPerformance)
class ContentPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "publication",
        "views",
        "likes",
        "comments",
        "shares",
        "retention_percent",
        "captured_at",
    )
    readonly_fields = ("captured_at",)
