from django.contrib import admin
from .models import AccountingEntry, Company, CompanyDelegation, Invoice, LedgerAccount, OfficeTask

admin.site.register(Company)
admin.site.register(CompanyDelegation)
admin.site.register(LedgerAccount)
admin.site.register(AccountingEntry)
admin.site.register(OfficeTask)
admin.site.register(Invoice)
