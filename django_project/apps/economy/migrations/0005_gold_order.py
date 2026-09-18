from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("economy", "0004_virtual_asset_economic_lifecycle")]
    operations = [migrations.CreateModel(
        name="GoldOrder",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("side", models.CharField(choices=[("buy","Buy"),("sell","Sell")], max_length=10)),
            ("product", models.CharField(default="gold_18", max_length=100)),
            ("weight_grams", models.DecimalField(decimal_places=6, max_digits=20)),
            ("quoted_price", models.DecimalField(blank=True, decimal_places=2, max_digits=24, null=True)),
            ("currency", models.CharField(default="IRR", max_length=10)),
            ("status", models.CharField(choices=[("draft","Draft"),("pending_approval","Pending owner approval"),("approved","Approved"),("quoted","Quoted"),("settled","Settled"),("cancelled","Cancelled"),("blocked","Blocked")], default="draft", max_length=30)),
            ("owner_approved", models.BooleanField(default=False)),
            ("provider_reference", models.CharField(blank=True, max_length=200)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="gold_orders", to="auth.user")),
        ],
    )]