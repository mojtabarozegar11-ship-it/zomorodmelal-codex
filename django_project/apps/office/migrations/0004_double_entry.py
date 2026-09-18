from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [("office", "0003_workflow_payroll_trade")]

    operations = [
        migrations.CreateModel(
            name="Journal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("journal_no", models.CharField(max_length=80)),
                ("entry_date", models.DateField()),
                ("description", models.CharField(blank=True, max_length=500)),
                ("status", models.CharField(choices=[("draft","پیش‌نویس"),("posted","ثبت‌شده"),("reversed","معکوس‌شده")], default="draft", max_length=20)),
                ("owner_approved", models.BooleanField(default=False)),
                ("posted_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="journals", to="office.company")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_journals", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="JournalLine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("line_no", models.PositiveIntegerField()),
                ("description", models.CharField(blank=True, max_length=300)),
                ("debit", models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ("credit", models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="journal_lines", to="office.ledgeraccount")),
                ("journal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lines", to="office.journal")),
            ],
        ),
        migrations.AddConstraint(model_name="journal", constraint=models.UniqueConstraint(fields=("company","journal_no"), name="office_journal_company_no_uniq")),
        migrations.AddConstraint(model_name="journalline", constraint=models.UniqueConstraint(fields=("journal","line_no"), name="office_journal_line_no_uniq")),
        migrations.AddConstraint(model_name="journalline", constraint=models.CheckConstraint(check=models.Q(debit__gte=0) & models.Q(credit__gte=0), name="office_journal_line_nonnegative")),
        migrations.AddConstraint(model_name="journalline", constraint=models.CheckConstraint(check=((models.Q(debit__gt=0) & models.Q(credit=0)) | (models.Q(debit=0) & models.Q(credit__gt=0))), name="office_journal_line_one_side")),
    ]