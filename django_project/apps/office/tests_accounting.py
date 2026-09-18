from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase

from .models import Company, CompanyDelegation, Journal, LedgerAccount
from .services import post_journal


class DoubleEntryJournalTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_superuser("owner", "owner@example.com", "pw")
        self.company = Company.objects.create(name="Test Co")
        CompanyDelegation.objects.create(
            company=self.company, user=self.owner, role="accountant",
            active=True, owner_approved=True
        )
        self.cash = LedgerAccount.objects.create(company=self.company, code="1000", name="Cash")
        self.sales = LedgerAccount.objects.create(company=self.company, code="4000", name="Sales")

    def test_balanced_journal_posts_atomically(self):
        journal = post_journal(
            company=self.company, journal_no="J-001", entry_date=date.today(),
            actor=self.owner, owner_approved=True,
            lines=[{"account": self.cash, "debit": Decimal("100.00")},
                   {"account": self.sales, "credit": Decimal("100.00")}],
        )
        self.assertEqual(journal.status, "posted")
        self.assertEqual(journal.lines.count(), 2)

    def test_unbalanced_journal_rolls_back(self):
        with self.assertRaises(ValidationError):
            post_journal(
                company=self.company, journal_no="J-002", entry_date=date.today(),
                actor=self.owner, owner_approved=True,
                lines=[{"account": self.cash, "debit": Decimal("100.00")}],
            )
        self.assertFalse(Journal.objects.filter(journal_no="J-002").exists())

    def test_owner_approval_is_required(self):
        with self.assertRaises(PermissionDenied):
            post_journal(
                company=self.company, journal_no="J-003", entry_date=date.today(),
                actor=self.owner, owner_approved=False,
                lines=[{"account": self.cash, "debit": Decimal("100.00")},
                       {"account": self.sales, "credit": Decimal("100.00")}],
            )

    def test_cross_company_account_is_rejected(self):
        other = Company.objects.create(name="Other Co")
        foreign = LedgerAccount.objects.create(company=other, code="2000", name="Foreign")
        with self.assertRaises(ValidationError):
            post_journal(
                company=self.company, journal_no="J-004", entry_date=date.today(),
                actor=self.owner, owner_approved=True,
                lines=[{"account": self.cash, "debit": Decimal("100.00")},
                       {"account": foreign, "credit": Decimal("100.00")}],
            )