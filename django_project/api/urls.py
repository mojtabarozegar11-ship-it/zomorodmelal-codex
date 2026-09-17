from django.urls import path
from .agent_api import agent_status, execute_goal
from .views import agent_execute

urlpatterns = [
    path("status/", agent_status),
    path("execute/", execute_goal),
    path("prepare/", agent_execute),
]
