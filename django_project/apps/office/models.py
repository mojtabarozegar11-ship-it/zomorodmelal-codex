from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=80, blank=True)
    national_id = models.CharField(max_length=80, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyDelegation(models.Model):
    ROLE_CHOICES = (("manager", "مدیر"), ("accountant", "حسابدار"), ("operator", "اپراتور"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="delegations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_delegations")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="operator")
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    owner_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} / {self.user}"


class LedgerAccount(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="ledger_accounts")
    account_type = models.CharField(max_length=30, default="general")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AccountingEntry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="entries")
    account = models.ForeignKey(LedgerAccount, on_delete=models.PROTECT, related_name="entries")
    description = models.CharField(max_length=300)
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    document_no = models.CharField(max_length=80, blank=True)
    entry_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        if self.account_id and self.company_id != self.account.company_id:
            from django.core.exceptions import ValidationError
            raise ValidationError({"account": "Account must belong to the same company."})


class Journal(models.Model):
    STATUS_CHOICES = (("draft", "پیش‌نویس"), ("posted", "ثبت‌شده"), ("reversed", "معکوس‌شده"))
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="journals")
    journal_no = models.CharField(max_length=80)
    entry_date = models.DateField()
    description = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_journals")
    owner_approved = models.BooleanField(default=False)
    posted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.journal_no


class JournalLine(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name="lines")
    line_no = models.PositiveIntegerField()
    account = models.ForeignKey(LedgerAccount, on_delete=models.PROTECT, related_name="journal_lines")
    description = models.CharField(max_length=300, blank=True)
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        ordering = ["line_no", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=("journal", "line_no"),
                name="office_journal_line_no_uniq",
            ),
            models.CheckConstraint(
                check=models.Q(debit__gte=0) & models.Q(credit__gte=0),
                name="office_journal_line_nonnegative",
            ),
            models.CheckConstraint(
                check=(
                    (models.Q(debit__gt=0) & models.Q(credit=0))
                    | (models.Q(debit=0) & models.Q(credit__gt=0))
                ),
                name="office_journal_line_one_side",
            ),
        ]

    def clean(self):
        if self.journal_id and self.account_id and self.journal.company_id != self.account.company_id:
            from django.core.exceptions import ValidationError
            raise ValidationError({"account": "Account must belong to the journal company."})


class OfficeTask(models.Model):
    STATUS_CHOICES = (("todo", "در انتظار"), ("doing", "در حال انجام"), ("done", "انجام شد"))
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    due_date = models.DateField(null=True, blank=True)
    owner_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="office_employee")
    personnel_code = models.CharField(max_length=50, unique=True)
    job_title = models.CharField(max_length=150, blank=True)
    base_salary = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    active = models.BooleanField(default=True)



class InventoryItem(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory_items")
    sku = models.CharField(max_length=80)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=30, default="عدد")
    quantity = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    reorder_point = models.DecimalField(max_digits=20, decimal_places=3, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("company", "sku"),
                name="office_inventory_company_sku_uniq",
            ),
        ]


class CashTransaction(models.Model):
    KIND_CHOICES = (("in", "دریافت"), ("out", "پرداخت"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="cash_transactions")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=300)
    transaction_date = models.DateField()
    reference = models.CharField(max_length=100, blank=True)



class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120)
    object_type = models.CharField(max_length=120)
    object_id = models.CharField(max_length=80, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    STATUS_CHOICES = (("draft", "پیش‌نویس"), ("issued", "صادرشده"), ("paid", "پرداخت‌شده"), ("cancelled", "لغوشده"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=80)
    party_name = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)



class WorkflowApproval(models.Model):
    STATUS_CHOICES = (("pending", "در انتظار"), ("approved", "تأیید"), ("rejected", "رد"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="workflow_approvals")
    title = models.CharField(max_length=250)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="workflow_requests")
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="workflow_approvals")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)


class PayrollRecord(models.Model):
    STATUS_CHOICES = (("draft", "پیش‌نویس"), ("approved", "تأیید"), ("paid", "پرداخت"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payroll_records")
    period = models.CharField(max_length=20)
    gross = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    net = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (("draft", "پیش‌نویس"), ("approved", "تأیید"), ("received", "دریافت"), ("cancelled", "لغو"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="purchase_orders")
    supplier = models.CharField(max_length=200)
    number = models.CharField(max_length=80)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    order_date = models.DateField()


class SalesOrder(models.Model):
    STATUS_CHOICES = (("draft", "پیش‌نویس"), ("confirmed", "تأیید"), ("delivered", "تحویل"), ("cancelled", "لغو"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sales_orders")
    customer = models.CharField(max_length=200)
    number = models.CharField(max_length=80)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    order_date = models.DateField()
