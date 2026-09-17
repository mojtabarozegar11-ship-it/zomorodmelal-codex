"""Health checks for Django to Agent integration."""

from django_integration.agent_service import AgentService


def integration_status():
    return {
        "django": "ready",
        "agent_service": AgentService.__name__,
        "status": "connected_layer"
    }
