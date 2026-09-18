from django.contrib import admin
from .models import ServiceCategory, ServiceOffering, ServiceRequest

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "order")
    list_filter = ("active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")

@admin.register(ServiceOffering)
class ServiceOfferingAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "service_type", "active", "request_enabled", "compliance_required", "owner_approval_required")
    list_filter = ("active", "request_enabled", "compliance_required", "owner_approval_required", "service_type", "category")
    search_fields = ("name", "slug", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("category__order", "order", "name")

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("tracking_code", "service", "user", "status", "owner_approved", "compliance_checked", "created_at")
    list_filter = ("status", "owner_approved", "compliance_checked", "service__category")
    search_fields = ("tracking_code", "user__username", "service__name", "details")
    readonly_fields = ("tracking_code", "created_at", "updated_at")
