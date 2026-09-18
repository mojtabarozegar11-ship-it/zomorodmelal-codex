from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("ai", "0002_content_agent")]

    operations = [
        migrations.CreateModel(
            name="ContentExperiment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("hypothesis", models.TextField(blank=True)),
                ("variant", models.CharField(default="A", max_length=80)),
                ("metrics", models.JSONField(blank=True, default=dict)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("publication", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="experiments", to="ai.contentpublication")),
            ],
        ),
    ]
