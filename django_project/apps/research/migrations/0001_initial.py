from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="ResearchProject", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("title", models.CharField(max_length=250)), ("summary", models.TextField(blank=True)), ("status", models.CharField(default="research", max_length=40)), ("owner_approval_required", models.BooleanField(default=True)), ("owner_approved", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True))])]
