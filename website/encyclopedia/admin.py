from django.contrib import admin
from .models import EncyclopediaCategory, EncyclopediaArticle, KnowledgeRelation

@admin.register(EncyclopediaCategory)
class EncyclopediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)

@admin.register(EncyclopediaArticle)
class EncyclopediaArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published', 'updated_at')
    search_fields = ('title', 'keywords')
    list_filter = ('published', 'category')

@admin.register(KnowledgeRelation)
class KnowledgeRelationAdmin(admin.ModelAdmin):
    list_display = ('source', 'target')
