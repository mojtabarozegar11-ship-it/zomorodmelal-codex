from django.urls import path

from . import content_agent_views

urlpatterns = [
    path("content-agent/", content_agent_views.content_agent_dashboard, name="content-agent-dashboard"),
    path("content-agent/brief/", content_agent_views.create_content_brief, name="content-agent-brief"),
    path(
        "content-agent/brief/<int:brief_id>/assets/",
        content_agent_views.generate_content_assets,
        name="content-agent-assets",
    ),
    path(
        "content-agent/brief/<int:brief_id>/approve/",
        content_agent_views.approve_content_brief,
        name="content-agent-brief-approve",
    ),
    path(
        "content-agent/brief/<int:brief_id>/queue/",
        content_agent_views.queue_content_publication,
        name="content-agent-queue",
    ),
    path(
        "content-agent/publication/<int:publication_id>/approve/",
        content_agent_views.approve_content_publication,
        name="content-agent-publication-approve",
    ),
    path(
        "content-agent/publication/<int:publication_id>/publish/",
        content_agent_views.publish_content,
        name="content-agent-publish",
    ),
]
