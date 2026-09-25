from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from .content_agent import ContentAgent
from .content_agent_models import (
    ContentAsset,
    ContentBrief,
    ContentChannel,
    ContentPublication,
)


class ContentPublicationApprovalGateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password"
        )
        self.staff = User.objects.create_user(
            username="staff", password="test-password", is_staff=True
        )
        self.channel = ContentChannel.objects.create(
            name="Test Channel",
            platform="website",
            topic="testing",
            owner_approved=False,
        )
        self.brief = ContentBrief.objects.create(
            channel=self.channel,
            topic="approval gates",
            status="approved",
            owner_approved=False,
            created_by=self.owner,
        )
        self.asset = ContentAsset.objects.create(
            brief=self.brief,
            asset_type="script",
            version=1,
            body="approved test content",
            approved=True,
        )
        self.publication = ContentPublication.objects.create(
            brief=self.brief,
            channel=self.channel,
            idempotency_key="content:test:1",
        )
        self.agent = ContentAgent()

    def test_publication_approval_requires_brief_and_channel_approval(self):
        with self.assertRaises(PermissionDenied):
            self.agent.approve_publication(
                self.publication, approved=True, actor=self.owner
            )

        self.brief.owner_approved = True
        self.brief.save(update_fields=["owner_approved"])
        with self.assertRaises(PermissionDenied):
            self.agent.approve_publication(
                self.publication, approved=True, actor=self.owner
            )

    def test_publish_rechecks_upstream_approval_gates(self):
        self.publication.owner_approved = True
        self.publication.save(update_fields=["owner_approved"])

        with self.assertRaises(PermissionDenied):
            self.agent.publish(self.publication, actor=self.owner)

        self.brief.owner_approved = True
        self.brief.save(update_fields=["owner_approved"])
        with self.assertRaises(PermissionDenied):
            self.agent.publish(self.publication, actor=self.owner)

    def test_owner_can_approve_and_publish_after_all_gates_pass(self):
        self.brief.owner_approved = True
        self.channel.owner_approved = True
        self.brief.save(update_fields=["owner_approved"])
        self.channel.save(update_fields=["owner_approved"])

        self.agent.approve_publication(
            self.publication, approved=True, actor=self.owner
        )
        self.agent.publish(self.publication, actor=self.owner)

        self.publication.refresh_from_db()
        self.assertEqual(self.publication.status, "published")
        self.assertTrue(self.publication.owner_approved)
