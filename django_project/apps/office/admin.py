from django.contrib import admin

from .models import (
    AccountingEntry, AuditLog, CashTransaction, Company, CompanyDelegation,
    Employee, InventoryItem, Invoice, Journal, JournalLine, LedgerAccount,
    OfficeTask, PayrollRecord, PurchaseOrder, SalesOrder, WorkflowApproval,
)

for model in (
    Company, CompanyDelegation, LedgerAccount, AccountingEntry, Journal, JournalLine,
    OfficeTask, Invoice, Employee, InventoryItem, CashTransaction, AuditLog,
    WorkflowApproval, PayrollRecord, PurchaseOrder, SalesOrder,
):
    admin.site.register(model)
