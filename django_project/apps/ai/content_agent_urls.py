from django.urls import path
from .content_agent_views import content_agent_dashboard, create_content_brief, publish_content, generate_content_assets

urlpatterns = [
    path("content-agent/", content_agent_dashboard, name="content-agent-dashboard"),
    path("content-agent/brief/", create_content_brief, name="content-agent-brief"),
    path("content-agent/publish/<int:publication_id>/", publish_content, name="content-agent-publish"),
    path("content-agent/brief/<int:brief_id>/assets/", generate_content_assets, name="content-agent-generate-assets"),
]
