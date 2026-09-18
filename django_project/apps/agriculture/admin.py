from django.contrib import admin

from .models import Farm, ProductionChain, ProductionProduct


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("name", "location")
    readonly_fields = ("created_at",)


@admin.register(ProductionProduct)
class ProductionProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "active")
    list_filter = ("active", "category")
    search_fields = ("name", "category")


@admin.register(ProductionChain)
class ProductionChainAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name", "description")
