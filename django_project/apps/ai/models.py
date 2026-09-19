from django.db import models


class AIConfiguration(models.Model):
    provider = models.CharField(max_length=50, unique=True)
    enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=500, blank=True, default="")
    base_url = models.URLField(blank=True, default="https://api.deepseek.com")
    model = models.CharField(max_length=100, default="deepseek-chat")
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.provider
