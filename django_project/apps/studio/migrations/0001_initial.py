from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="StudioIdea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("source", models.CharField(default="master-agent", max_length=100)),
                ("explored", models.BooleanField(default=False)),
                ("approved_for_prototyping", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-created_at",), "verbose_name": "ایده استودیو", "verbose_name_plural": "ایده‌های استودیو"},
        ),
        migrations.CreateModel(
            name="StudioProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("kind", models.CharField(choices=[("game", "بازی"), ("app", "اپلیکیشن")], max_length=20)),
                ("status", models.CharField(choices=[("idea", "ایده"), ("research", "مطالعه"), ("design", "طراحی"), ("prototype", "نمونه اولیه"), ("development", "توسعه"), ("testing", "آزمون"), ("release_ready", "آماده انتشار"), ("published", "منتشرشده"), ("maintenance", "توسعه پس از انتشار")], default="idea", max_length=30)),
                ("concept", models.TextField(blank=True)),
                ("business_model", models.TextField(blank=True)),
                ("research_notes", models.TextField(blank=True)),
                ("innovation_notes", models.TextField(blank=True)),
                ("owner_approval_required", models.BooleanField(default=True)),
                ("real_release_approved", models.BooleanField(default=False)),
                ("nft_enabled", models.BooleanField(default=False)),
                ("nft_release_approved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("-updated_at",), "verbose_name": "پروژه استودیو", "verbose_name_plural": "پروژه‌های استودیو"},
        ),
        migrations.CreateModel(
            name="StudioMilestone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("done", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="milestones", to="studio.studioproject")),
            ],
            options={"ordering": ("created_at",), "verbose_name": "مرحله استودیو", "verbose_name_plural": "مراحل استودیو"},
        ),
    ]
