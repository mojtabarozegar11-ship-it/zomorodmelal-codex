from django.urls import path
from .agent_api import agent_status, execute_goal
from apps.ai.mobile_admin import mobile_admin, mobile_icon, mobile_manifest, mobile_service_worker

urlpatterns = [
    path("status/", agent_status),
    path("execute/", execute_goal),
]
