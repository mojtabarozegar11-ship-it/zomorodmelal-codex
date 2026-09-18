from django.db import models


class ResearchProject(models.Model):
    title = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=40, default="research")
    owner_approval_required = models.BooleanField(default=True)
    owner_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
