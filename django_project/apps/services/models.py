from django.conf import settings
from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "دسته خدمت"
        verbose_name_plural = "دسته‌های خدمات"

    def __str__(self):
        return self.name


class ServiceOffering(models.Model):
    TYPE_CHOICES = [
        ("request", "درخواستی"),
        ("quote", "استعلام قیمت"),
        ("info", "اطلاعاتی"),
    ]
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="services")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    service_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="request")
    requires_quote = models.BooleanField(default=True)
    request_enabled = models.BooleanField(default=True)
    compliance_required = models.BooleanField(default=False)
    owner_approval_required = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("category__order", "order", "name")
        constraints = [
            models.UniqueConstraint(fields=("category", "name"), name="unique_service_name_per_category")
        ]
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("submitted", "ثبت شد"),
        ("review", "در حال بررسی"),
        ("quoted", "قیمت اعلام شد"),
        ("approved", "تأیید شد"),
        ("in_progress", "در حال انجام"),
        ("completed", "انجام شد"),
        ("cancelled", "لغو شد"),
        ("blocked", "متوقف شد"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="service_requests")
    service = models.ForeignKey(ServiceOffering, on_delete=models.PROTECT, related_name="requests")
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    quote_amount = models.DecimalField(max_digits=24, decimal_places=2, null=True, blank=True)
    quote_currency = models.CharField(max_length=10, default="IRR")
    owner_approved = models.BooleanField(default=False)
    compliance_checked = models.BooleanField(default=False)
    tracking_code = models.CharField(max_length=32, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "درخواست خدمت"
        verbose_name_plural = "درخواست‌های خدمات"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            import secrets
            self.tracking_code = "ZM-" + secrets.token_hex(6).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_code
