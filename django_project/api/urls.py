from django.urls import path
from .agent_api import agent_status, execute_goal, health, agent_dashboard
from .agent_service_view import execute_agent_goal, worker_health

urlpatterns = [
    path("dashboard/", agent_dashboard, name="agent-dashboard"),
    path("status/", agent_status, name="agent-status"),
    path("execute/", execute_goal, name="execute-goal"),
    path("execute-worker/", execute_agent_goal, name="execute-worker"),
    path("worker-health/", worker_health, name="worker-health"),
    path("health/", health, name="health"),
]
