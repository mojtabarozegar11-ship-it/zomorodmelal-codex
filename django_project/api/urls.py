from django.urls import path
from .agent_api import agent_status, execute_goal, health, agent_dashboard

urlpatterns = [
    path("dashboard/", agent_dashboard, name="agent-dashboard"),
    path("status/", agent_status, name="agent-status"),
    path("execute/", execute_goal, name="execute-goal"),
    path("health/", health, name="health"),
]
