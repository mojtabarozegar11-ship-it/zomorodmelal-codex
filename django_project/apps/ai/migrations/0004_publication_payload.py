from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("ai", "0003_content_experiment")]
    operations = [
        migrations.AddField(
            model_name="contentpublication",
            name="payload",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
