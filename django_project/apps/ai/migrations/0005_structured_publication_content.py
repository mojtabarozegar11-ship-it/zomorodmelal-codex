from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("ai", "0004_publication_payload")]
    operations = [
        migrations.AddField(
            model_name="contentpublication",
            name="content_json",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
