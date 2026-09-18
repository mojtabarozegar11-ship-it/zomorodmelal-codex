from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [("economy", "0005_gold_order")]
    operations = [migrations.AlterModelOptions(name="marketdatasnapshot", options={"ordering": ["-timestamp"]})]
