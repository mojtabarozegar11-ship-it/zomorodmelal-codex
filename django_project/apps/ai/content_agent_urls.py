from django.urls import path
from .content_agent_views import content_agent_dashboard, create_content_brief, publish_content

urlpatterns = [
    path("content-agent/", content_agent_dashboard, name="content-agent-dashboard"),
    path("content-agent/brief/", create_content_brief, name="content-agent-brief"),
    path("content-agent/publish/<int:publication_id>/", publish_content, name="content-agent-publish"),
]
