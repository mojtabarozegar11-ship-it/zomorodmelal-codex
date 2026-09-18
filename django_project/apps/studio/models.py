from django.db import models


class StudioProject(models.Model):
    KIND_CHOICES = (("game", "بازی"), ("app", "اپلیکیشن"))
    STATUS_CHOICES = (
        ("idea", "ایده"),
        ("research", "مطالعه"),
        ("design", "طراحی"),
        ("prototype", "نمونه اولیه"),
        ("development", "توسعه"),
        ("testing", "آزمون"),
        ("release_ready", "آماده انتشار"),
        ("published", "منتشرشده"),
        ("maintenance", "توسعه پس از انتشار"),
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="idea")
    concept = models.TextField(blank=True)
    business_model = models.TextField(blank=True)
    research_notes = models.TextField(blank=True)
    innovation_notes = models.TextField(blank=True)
    owner_approval_required = models.BooleanField(default=True)
    real_release_approved = models.BooleanField(default=False)
    nft_enabled = models.BooleanField(default=False)
    nft_release_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        verbose_name = "پروژه استودیو"
        verbose_name_plural = "پروژه‌های استودیو"

    def __str__(self):
        return self.name


class StudioIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    source = models.CharField(max_length=100, default="master-agent")
    explored = models.BooleanField(default=False)
    approved_for_prototyping = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "ایده استودیو"
        verbose_name_plural = "ایده‌های استودیو"

    def __str__(self):
        return self.title


class StudioMilestone(models.Model):
    project = models.ForeignKey(
        StudioProject,
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "مرحله استودیو"
        verbose_name_plural = "مراحل استودیو"

    def __str__(self):
        return f"{self.project.name}: {self.title}"
