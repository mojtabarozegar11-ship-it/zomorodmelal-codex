from django.contrib import admin

from .models import (
    AccountingEntry,
    AuditLog,
    CashTransaction,
    Company,
    CompanyDelegation,
    Employee,
    InventoryItem,
    Invoice,
    Journal,
    JournalLine,
    LedgerAccount,
    OfficeTask,
    PayrollRecord,
    PurchaseOrder,
    SalesOrder,
    WorkflowApproval,
)

admin.site.register(Company)
admin.site.register(CompanyDelegation)
admin.site.register(LedgerAccount)
admin.site.register(AccountingEntry)
admin.site.register(Journal)
admin.site.register(JournalLine)
admin.site.register(OfficeTask)
admin.site.register(Invoice)
admin.site.register(Employee)
admin.site.register(InventoryItem)
admin.site.register(CashTransaction)
admin.site.register(AuditLog)
admin.site.register(WorkflowApproval)
admin.site.register(PayrollRecord)
admin.site.register(PurchaseOrder)
admin.site.register(SalesOrder)
