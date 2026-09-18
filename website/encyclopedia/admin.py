from django.contrib import admin
from .models import EncyclopediaCategory, EncyclopediaArticle, KnowledgeRelation


@admin.register(EncyclopediaCategory)
class EncyclopediaCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")


@admin.register(EncyclopediaArticle)
class EncyclopediaArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published", "updated_at")
    search_fields = ("title", "keywords", "content")
    list_filter = ("published", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(KnowledgeRelation)
class KnowledgeRelationAdmin(admin.ModelAdmin):
    list_display = ("article", "related_article")
    search_fields = ("article__title", "related_article__title")
