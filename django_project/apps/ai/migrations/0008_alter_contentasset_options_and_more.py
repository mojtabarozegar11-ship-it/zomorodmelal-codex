from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [("ai", "0007_alter_contentasset_options_and_more")]
    operations = [
        migrations.AlterModelOptions(
            name="contentasset",
            options={"ordering": ("asset_type", "-version")},
        ),
        migrations.AlterModelOptions(
            name="contentpublication",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AlterModelOptions(
            name="seoblogitem",
            options={"ordering": ("blog__name", "language")},
        ),
    ]
