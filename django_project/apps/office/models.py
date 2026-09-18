from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=80, blank=True)
    national_id = models.CharField(max_length=80, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت‌ها"

    def __str__(self):
        return self.name


class CompanyDelegation(models.Model):
    ROLE_CHOICES = [("manager", "مدیر"), ("accountant", "حسابدار"), ("operator", "اپراتور")]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="delegations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_delegations")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="operator")
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    owner_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("company", "user")
        verbose_name = "واگذاری دسترسی شرکت"
        verbose_name_plural = "واگذاری‌های دسترسی شرکت"

    def __str__(self):
        return f"{self.company} / {self.user}"


class LedgerAccount(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="ledger_accounts")
    account_type = models.CharField(max_length=30, default="general")
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "code")
        verbose_name = "حساب دفترکل"
        verbose_name_plural = "حساب‌های دفترکل"

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

    class Meta:
        ordering = ("-entry_date", "-id")
        verbose_name = "سند حسابداری"
        verbose_name_plural = "اسناد حسابداری"


class OfficeTask(models.Model):
    STATUS_CHOICES = [("todo", "در انتظار"), ("doing", "در حال انجام"), ("done", "انجام شد")]
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    due_date = models.DateField(null=True, blank=True)
    owner_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("status", "due_date", "-created_at")
        verbose_name = "وظیفه اداری"
        verbose_name_plural = "وظایف اداری"


class Invoice(models.Model):
    STATUS_CHOICES = [("draft", "پیش‌نویس"), ("issued", "صادرشده"), ("paid", "پرداخت‌شده"), ("cancelled", "لغوشده")]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=80)
    party_name = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("company", "number")
        ordering = ("-issue_date", "-id")
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"
