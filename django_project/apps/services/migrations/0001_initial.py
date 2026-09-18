from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings



class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="ServiceCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ("order", "name"), "verbose_name": "دسته خدمت", "verbose_name_plural": "دسته‌های خدمات"},
        ),
        migrations.CreateModel(
            name="ServiceOffering",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("summary", models.CharField(blank=True, max_length=300)),
                ("description", models.TextField(blank=True)),
                ("service_type", models.CharField(choices=[("request","درخواستی"),("quote","استعلام قیمت"),("info","اطلاعاتی")], default="request", max_length=20)),
                ("requires_quote", models.BooleanField(default=True)),
                ("request_enabled", models.BooleanField(default=True)),
                ("compliance_required", models.BooleanField(default=False)),
                ("owner_approval_required", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="services", to="services.servicecategory")),
            ],
            options={"ordering": ("category__order","order","name"), "verbose_name":"خدمت", "verbose_name_plural":"خدمات"},
        ),
        migrations.AddConstraint(
            model_name="serviceoffering",
            constraint=models.UniqueConstraint(fields=("category","name"), name="unique_service_name_per_category"),
        ),
        migrations.CreateModel(
            name="ServiceRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("details", models.TextField()),
                ("status", models.CharField(choices=[("submitted","ثبت شد"),("review","در حال بررسی"),("quoted","قیمت اعلام شد"),("approved","تأیید شد"),("in_progress","در حال انجام"),("completed","انجام شد"),("cancelled","لغو شد"),("blocked","متوقف شد")], default="submitted", max_length=20)),
                ("quote_amount", models.DecimalField(blank=True, decimal_places=2, max_digits=24, null=True)),
                ("quote_currency", models.CharField(default="IRR", max_length=10)),
                ("owner_approved", models.BooleanField(default=False)),
                ("compliance_checked", models.BooleanField(default=False)),
                ("tracking_code", models.CharField(editable=False, max_length=32, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="requests", to="services.serviceoffering")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="service_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",), "verbose_name":"درخواست خدمت", "verbose_name_plural":"درخواست‌های خدمات"},
        ),
    ]
