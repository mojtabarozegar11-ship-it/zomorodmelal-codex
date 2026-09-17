"""Internal Django API bridge for Master Agent.

Provides a simple interface layer between Django services and Agent Core.
"""

from django.http import JsonResponse


def agent_status(request):
    return JsonResponse({
        "service": "master_agent_bridge",
        "status": "ready"
    })


def execute_goal(request):
    return JsonResponse({
        "goal": None,
        "status": "pending_agent_connection"
    })
