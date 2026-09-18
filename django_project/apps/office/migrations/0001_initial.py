from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(name="Company", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=200)), ("registration_number", models.CharField(blank=True, max_length=80)),
            ("national_id", models.CharField(blank=True, max_length=80)), ("active", models.BooleanField(default=True)),
            ("created_at", models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name="LedgerAccount", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("code", models.CharField(max_length=30)), ("name", models.CharField(max_length=200)),
            ("account_type", models.CharField(default="general", max_length=30)), ("active", models.BooleanField(default=True)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ledger_accounts", to="office.company"))]),
        migrations.CreateModel(name="CompanyDelegation", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("role", models.CharField(choices=[("manager", "مدیر"), ("accountant", "حسابدار"), ("operator", "اپراتور")], default="operator", max_length=20)),
            ("active", models.BooleanField(default=True)), ("starts_at", models.DateTimeField(auto_now_add=True)), ("ends_at", models.DateTimeField(blank=True, null=True)),
            ("owner_approved", models.BooleanField(default=False)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="delegations", to="office.company")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="company_delegations", to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name="OfficeTask", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=250)), ("description", models.TextField(blank=True)),
            ("status", models.CharField(choices=[("todo", "در انتظار"), ("doing", "در حال انجام"), ("done", "انجام شد")], default="todo", max_length=20)),
            ("due_date", models.DateField(blank=True, null=True)), ("owner_approved", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("assigned_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ("company", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="office.company"))]),
        migrations.CreateModel(name="Invoice", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("number", models.CharField(max_length=80)),
            ("party_name", models.CharField(max_length=200)), ("total", models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ("status", models.CharField(choices=[("draft", "پیش‌نویس"), ("issued", "صادرشده"), ("paid", "پرداخت‌شده"), ("cancelled", "لغوشده")], default="draft", max_length=20)),
            ("issue_date", models.DateField()), ("due_date", models.DateField(blank=True, null=True)),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="invoices", to="office.company"))]),
        migrations.CreateModel(name="AccountingEntry", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("description", models.CharField(max_length=300)),
            ("debit", models.DecimalField(decimal_places=2, default=0, max_digits=20)), ("credit", models.DecimalField(decimal_places=2, default=0, max_digits=20)),
            ("document_no", models.CharField(blank=True, max_length=80)), ("entry_date", models.DateField()), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("account", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="entries", to="office.ledgeraccount")),
            ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="entries", to="office.company")),
            ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))]),
    ]
