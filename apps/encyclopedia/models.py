from django.db import models


class EncyclopediaCategory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )

    def __str__(self):
        return self.title


class KnowledgeArticle(models.Model):
    category = models.ForeignKey(
        EncyclopediaCategory,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    references = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class KnowledgeRelation(models.Model):
    source = models.ForeignKey(
        KnowledgeArticle,
        on_delete=models.CASCADE,
        related_name='relations'
    )
    target = models.ForeignKey(
        KnowledgeArticle,
        on_delete=models.CASCADE,
        related_name='related_from'
    )
    relation_type = models.CharField(max_length=100, blank=True)
