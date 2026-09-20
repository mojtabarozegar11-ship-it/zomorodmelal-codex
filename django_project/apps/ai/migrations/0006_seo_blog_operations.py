from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ai", "0005_structured_publication_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPlatform",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180, unique=True)),
                ("platform", models.CharField(max_length=80)),
                ("base_url", models.URLField()),
                ("language", models.CharField(default="en", max_length=30)),
                ("signup_url", models.URLField(blank=True)),
                ("publish_url", models.URLField(blank=True)),
                ("api_endpoint", models.URLField(blank=True)),
                ("active", models.BooleanField(default=True)),
                ("legal_terms_reviewed", models.BooleanField(default=False)),
                ("account_ready", models.BooleanField(default=False)),
                ("credentials_configured", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="SeoBlogRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("run_date", models.DateField()),
                ("scheduled_time", models.TimeField()),
                ("status", models.CharField(choices=[("planned","Planned"),("running","Running"),("completed","Completed"),("partial","Partial"),("failed","Failed")], default="planned", max_length=20)),
                ("target_languages", models.JSONField(blank=True, default=list)),
                ("target_count", models.PositiveIntegerField(default=5)),
                ("published_count", models.PositiveIntegerField(default=0)),
                ("pending_count", models.PositiveIntegerField(default=0)),
                ("failed_count", models.PositiveIntegerField(default=0)),
                ("report", models.JSONField(blank=True, default=dict)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-run_date", "-scheduled_time")},
        ),
        migrations.CreateModel(
            name="SeoBlogItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(max_length=30)),
                ("topic", models.CharField(max_length=300)),
                ("title", models.CharField(max_length=300)),
                ("body", models.TextField()),
                ("seo_metadata", models.JSONField(blank=True, default=dict)),
                ("external_url", models.URLField(blank=True)),
                ("status", models.CharField(choices=[("draft","Draft"),("ready","Ready"),("published","Published"),("pending_access","Pending access"),("failed","Failed")], default="draft", max_length=30)),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("blog", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="items", to="ai.blogplatform")),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="ai.seoblogrun")),
            ],
            options={"ordering": ("blog", "language")},
        ),
        migrations.AddConstraint(
            model_name="seoblogrun",
            constraint=models.UniqueConstraint(fields=("run_date", "scheduled_time"), name="ai_seo_blog_run_date_time_uniq"),
        ),
        migrations.AddConstraint(
            model_name="seoblogitem",
            constraint=models.UniqueConstraint(fields=("run", "blog"), name="ai_seo_blog_item_run_blog_uniq"),
        ),
    ]
