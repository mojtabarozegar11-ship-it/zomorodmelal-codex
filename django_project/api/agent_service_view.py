"""Django endpoint adapter for the unified Worker/Master runtime."""
import json

from django.http import JsonResponse

from django_integration.agent_service import AgentService


service = AgentService()


def execute_agent_goal(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        body = {}

    goal = body.get("goal") or request.POST.get("goal")
    if not goal:
        return JsonResponse({"status": "error", "message": "goal required"}, status=400)

    approved = bool(body.get("approved", False))
    context = body.get("context") or {}
    return JsonResponse(service.run(goal, context=context, approved=approved))


def worker_health(request):
    return JsonResponse(service.health())
