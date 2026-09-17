"""Django endpoint adapter for Agent Service."""

from django.http import JsonResponse

from django_integration.agent_service import AgentService


service = AgentService()


def execute_agent_goal(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)

    goal = request.POST.get("goal")
    if not goal:
        return JsonResponse({"status": "error", "message": "goal required"}, status=400)

    result = service.run(goal)
    return JsonResponse(result)
