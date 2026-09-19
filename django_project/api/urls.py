from django.urls import path

from .agent_api import (
    agent_dashboard,
    agent_status,
    api_v1_discovery,
    api_v1_execute,
    api_v1_health,
    api_v1_status,
    execute_goal,
    health,
)

urlpatterns = [
    path("dashboard/", agent_dashboard, name="agent-dashboard"),
    path("status/", agent_status, name="agent-status"),
    path("execute/", execute_goal, name="execute-goal"),
    path("health/", health, name="health"),
    path("v1/", api_v1_discovery, name="api-v1-discovery"),
    path("v1/status/", api_v1_status, name="api-v1-status"),
    path("v1/health/", api_v1_health, name="api-v1-health"),
    path("v1/agent/execute/", api_v1_execute, name="api-v1-agent-execute"),
]
