"""Worker health endpoint for the unified runtime."""
from django.http import JsonResponse

from django_integration.agent_service import AgentService

service = AgentService()


def worker_health(request):
    if request.method != "GET":
        return JsonResponse({"status": "error", "message": "GET required"}, status=405)
    return JsonResponse(service.health())
