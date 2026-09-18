from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("office", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Employee", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("personnel_code", models.CharField(max_length=50, unique=True)), ("job_title", models.CharField(blank=True, max_length=150)),
            ("base_salary", models.DecimalField(decimal_places=2, default=0, max_digits=20)), ("active", models.BooleanField(default=True)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="employees", to="office.company")),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="office_employee", to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name="InventoryItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("sku", models.CharField(max_length=80)),
            ("name", models.CharField(max_length=200)), ("unit", models.CharField(default="عدد", max_length=30)), ("quantity", models.DecimalField(decimal_places=3, default=0, max_digits=20)), ("reorder_point", models.DecimalField(decimal_places=3, default=0, max_digits=20)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inventory_items", to="office.company"))]),
        migrations.CreateModel(name="CashTransaction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("kind", models.CharField(choices=[("in", "دریافت"), ("out", "پرداخت")], max_length=10)),
            ("amount", models.DecimalField(decimal_places=2, max_digits=20)), ("description", models.CharField(max_length=300)), ("transaction_date", models.DateField()), ("reference", models.CharField(blank=True, max_length=100)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cash_transactions", to="office.company"))]),
        migrations.CreateModel(name="AuditLog", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("action", models.CharField(max_length=120)), ("object_type", models.CharField(max_length=120)), ("object_id", models.CharField(blank=True, max_length=80)), ("metadata", models.JSONField(blank=True, default=dict)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("actor", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)), ("company", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="office.company"))]),
        migrations.AddConstraint(model_name="inventoryitem", constraint=models.UniqueConstraint(fields=("company", "sku"), name="office_inventory_company_sku_uniq")),
    ]
