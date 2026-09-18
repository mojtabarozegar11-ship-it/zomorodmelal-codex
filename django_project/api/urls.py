from django.urls import path
from .agent_api import agent_status, execute_goal

urlpatterns=[path("status/", agent_status), path("execute/", execute_goal)]
