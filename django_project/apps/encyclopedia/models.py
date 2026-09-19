from django.db import models


class EncyclopediaCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class EncyclopediaArticle(models.Model):
    category = models.ForeignKey(EncyclopediaCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    keywords = models.TextField(blank=True)
    sources = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "title")

    def __str__(self):
        return self.title


class KnowledgeRelation(models.Model):
    article = models.ForeignKey(
        EncyclopediaArticle,
        related_name="outgoing_relations",
        on_delete=models.CASCADE,
    )
    related_article = models.ForeignKey(
        EncyclopediaArticle,
        related_name="incoming_relations",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("article", "related_article"),
                name="encyclopedia_relation_unique",
            ),
        ]

    def __str__(self):
        return f"{self.article} -> {self.related_article}"
