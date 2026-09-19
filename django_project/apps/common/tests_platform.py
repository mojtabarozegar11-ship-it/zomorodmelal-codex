from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from .models import PlatformAuditEvent
from .platform import approve_owner_action, require_owner_actor, require_owner_approval


class GovernanceBoundaryTests(TestCase):
    def test_owner_approval_rejects_false(self):
        with self.assertRaises(PermissionDenied):
            require_owner_approval(False)

    def test_owner_actor_requires_superuser(self):
        user = get_user_model().objects.create_user(
            username="operator", password="pass"
        )
        with self.assertRaises(PermissionDenied):
            require_owner_actor(user)

    def test_owner_actor_accepts_superuser(self):
        owner = get_user_model().objects.create_superuser(
            username="owner", email="owner@example.com", password="pass"
        )
        self.assertEqual(require_owner_actor(owner), owner)

    def test_owner_approval_creates_audit_event(self):
        owner = get_user_model().objects.create_superuser(
            username="owner2", email="owner2@example.com", password="pass"
        )
        event = approve_owner_action(
            actor=owner,
            action="test_approval",
            scope="common.governance",
            metadata={"source": "test"},
        )
        self.assertIsInstance(event, PlatformAuditEvent)
        self.assertTrue(event.metadata["owner_approved"])
