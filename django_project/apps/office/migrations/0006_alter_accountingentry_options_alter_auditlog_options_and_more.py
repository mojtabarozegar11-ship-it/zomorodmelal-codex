from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("office", "0005_alter_accountingentry_options_alter_auditlog_options_and_more")]
    operations = [
        migrations.AlterModelOptions(name="accountingentry", options={"ordering": ("-entry_date", "-id"), "verbose_name": "سند حسابداری", "verbose_name_plural": "اسناد حسابداری"}),
        migrations.AlterModelOptions(name="auditlog", options={"ordering": ("-created_at",), "verbose_name": "لاگ حسابرسی", "verbose_name_plural": "لاگ‌های حسابرسی"}),
        migrations.AlterModelOptions(name="cashtransaction", options={"ordering": ("-transaction_date", "-id"), "verbose_name": "تراکنش خزانه", "verbose_name_plural": "تراکنش‌های خزانه"}),
        migrations.AlterModelOptions(name="company", options={"ordering": ("name",), "verbose_name": "شرکت", "verbose_name_plural": "شرکت‌ها"}),
        migrations.AlterModelOptions(name="companydelegation", options={"verbose_name": "واگذاری دسترسی شرکت", "verbose_name_plural": "واگذاری‌های دسترسی شرکت"}),
        migrations.AlterModelOptions(name="employee", options={"verbose_name": "کارمند", "verbose_name_plural": "کارکنان"}),
        migrations.AlterModelOptions(name="inventoryitem", options={"verbose_name": "قلم انبار", "verbose_name_plural": "اقلام انبار"}),
        migrations.AlterModelOptions(name="invoice", options={"ordering": ("-issue_date", "-id"), "verbose_name": "فاکتور", "verbose_name_plural": "فاکتورها"}),
        migrations.AlterModelOptions(name="journal", options={"ordering": ("-entry_date", "-id"), "verbose_name": "سند دفتر روزنامه", "verbose_name_plural": "اسناد دفتر روزنامه"}),
        migrations.AlterModelOptions(name="journalline", options={"ordering": ("line_no", "id")}),
        migrations.AlterModelOptions(name="ledgeraccount", options={"verbose_name": "حساب دفترکل", "verbose_name_plural": "حساب‌های دفترکل"}),
        migrations.AlterModelOptions(name="officetask", options={"ordering": ("status", "due_date", "-created_at"), "verbose_name": "وظیفه اداری", "verbose_name_plural": "وظایف اداری"}),
        migrations.RemoveConstraint(model_name="inventoryitem", name="office_inventory_company_sku_uniq"),
        migrations.AlterUniqueTogether(name="companydelegation", unique_together={("company", "user")}),
        migrations.AlterUniqueTogether(name="inventoryitem", unique_together={("company", "sku")}),
        migrations.AlterUniqueTogether(name="invoice", unique_together={("company", "number")}),
        migrations.AlterUniqueTogether(name="ledgeraccount", unique_together={("company", "code")}),
        migrations.AddConstraint(model_name="accountingentry", constraint=models.CheckConstraint(check=models.Q(debit__gte=0) & models.Q(credit__gte=0), name="office_entry_nonnegative")),
        migrations.AddConstraint(model_name="accountingentry", constraint=models.CheckConstraint(check=((models.Q(debit__gt=0) & models.Q(credit=0)) | (models.Q(debit=0) & models.Q(credit__gt=0))), name="office_entry_one_side")),
        migrations.AddConstraint(model_name="cashtransaction", constraint=models.CheckConstraint(check=models.Q(amount__gt=0), name="office_cash_amount_positive")),
        migrations.AddConstraint(model_name="employee", constraint=models.CheckConstraint(check=models.Q(base_salary__gte=0), name="office_employee_salary_nonnegative")),
        migrations.AddConstraint(model_name="invoice", constraint=models.CheckConstraint(check=models.Q(total__gte=0), name="office_invoice_total_nonnegative")),
    ]
