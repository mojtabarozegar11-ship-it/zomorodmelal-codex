from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("common", "0001_platform_core")]

    operations = [
        migrations.AlterField(
            model_name="idempotencyrecord",
            name="key",
            field=models.CharField(max_length=180),
        ),
        migrations.AddConstraint(
            model_name="idempotencyrecord",
            constraint=models.UniqueConstraint(
                fields=("actor", "scope", "key"),
                name="common_idempotency_actor_scope_key_uniq",
            ),
        ),
    ]
