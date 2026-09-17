from django.db import models


class SitePage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ActivityLog(models.Model):
    action = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action
