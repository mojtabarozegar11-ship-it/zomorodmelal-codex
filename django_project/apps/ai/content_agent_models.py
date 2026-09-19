from django.conf import settings
from django.db import models


class ContentChannel(models.Model):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("telegram", "Telegram"),
        ("x", "X"),
        ("facebook", "Facebook"),
        ("linkedin", "LinkedIn"),
        ("website", "Website"),
    ]
    name = models.CharField(max_length=180)
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    handle = models.CharField(max_length=180, blank=True)
    topic = models.CharField(max_length=250)
    audience = models.TextField(blank=True)
    language = models.CharField(max_length=30, default="fa")
    tone = models.CharField(max_length=80, default="professional")
    posting_frequency = models.PositiveIntegerField(default=3)
    timezone = models.CharField(max_length=80, default="Asia/Tehran")
    active = models.BooleanField(default=True)
    auto_publish = models.BooleanField(default=False)
    owner_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ("platform", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("platform", "name"),
                name="ai_channel_platform_name_uniq",
            ),
        ]

    def __str__(self):
        return self.name


class ContentCompetitor(models.Model):
    channel = models.ForeignKey(ContentChannel, on_delete=models.CASCADE, related_name="competitors")
    name = models.CharField(max_length=180)
    platform = models.CharField(max_length=30)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContentStrategy(models.Model):
    channel = models.OneToOneField(ContentChannel, on_delete=models.CASCADE, related_name="strategy")
    pillars = models.JSONField(default=list, blank=True)
    audience_personas = models.JSONField(default=list, blank=True)
    formats = models.JSONField(default=list, blank=True)
    hooks = models.JSONField(default=list, blank=True)
    banned_topics = models.JSONField(default=list, blank=True)
    brand_rules = models.JSONField(default=dict, blank=True)
    algorithm_notes = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContentResearchSnapshot(models.Model):
    channel = models.ForeignKey(ContentChannel, on_delete=models.CASCADE, related_name="research_snapshots")
    query = models.CharField(max_length=300)
    source = models.CharField(max_length=120)
    url = models.URLField(blank=True)
    title = models.CharField(max_length=300, blank=True)
    summary = models.TextField(blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-captured_at",)


class ContentBrief(models.Model):
    STATUS_CHOICES = [
        ("idea", "Idea"), ("research", "Research"), ("briefed", "Briefed"),
        ("drafting", "Drafting"), ("review", "Review"), ("approved", "Approved"),
        ("scheduled", "Scheduled"), ("published", "Published"), ("failed", "Failed"),
    ]
    channel = models.ForeignKey(ContentChannel, on_delete=models.CASCADE, related_name="briefs")
    topic = models.CharField(max_length=300)
    objective = models.CharField(max_length=200, blank=True)
    format = models.CharField(max_length=80, default="short_video")
    angle = models.TextField(blank=True)
    audience_pain = models.TextField(blank=True)
    hook = models.TextField(blank=True)
    call_to_action = models.TextField(blank=True)
    keywords = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="idea")
    scorecard = models.JSONField(default=dict, blank=True)
    owner_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContentAsset(models.Model):
    ASSET_TYPES = [
        ("script", "Script"), ("caption", "Caption"), ("title", "Title"),
        ("description", "Description"), ("thumbnail_prompt", "Thumbnail prompt"),
        ("hashtags", "Hashtags"), ("carousel", "Carousel"), ("image_prompt", "Image prompt"),
    ]
    brief = models.ForeignKey(ContentBrief, on_delete=models.CASCADE, related_name="assets")
    asset_type = models.CharField(max_length=40, choices=ASSET_TYPES)
    version = models.PositiveIntegerField(default=1)
    body = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class ContentPublication(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"), ("scheduled", "Scheduled"), ("publishing", "Publishing"),
        ("published", "Published"), ("failed", "Failed"), ("cancelled", "Cancelled"),
    ]
    brief = models.ForeignKey(ContentBrief, on_delete=models.PROTECT, related_name="publications")
    channel = models.ForeignKey(ContentChannel, on_delete=models.PROTECT, related_name="publications")
    scheduled_for = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    content_json = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    provider = models.CharField(max_length=60, default="manual")
    external_id = models.CharField(max_length=180, blank=True)
    idempotency_key = models.CharField(max_length=180, unique=True)
    response_metadata = models.JSONField(default=dict, blank=True)
    owner_approved = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)


class ContentPerformance(models.Model):
    publication = models.OneToOneField(ContentPublication, on_delete=models.CASCADE, related_name="performance")
    impressions = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    likes = models.PositiveBigIntegerField(default=0)
    comments = models.PositiveBigIntegerField(default=0)
    shares = models.PositiveBigIntegerField(default=0)
    saves = models.PositiveBigIntegerField(default=0)
    watch_time_seconds = models.FloatField(default=0)
    retention_percent = models.FloatField(default=0)
    click_through_rate = models.FloatField(default=0)
    followers_gained = models.IntegerField(default=0)
    captured_at = models.DateTimeField(auto_now=True)


class ContentExperiment(models.Model):
    publication = models.ForeignKey(ContentPublication, on_delete=models.CASCADE, related_name="experiments")
    name = models.CharField(max_length=160)
    hypothesis = models.TextField(blank=True)
    variant = models.CharField(max_length=80, default="A")
    metrics = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
