"""HTTP bridge between Django and the safe Master Agent runtime."""
import json
from django.http import JsonResponse
from autonomous_core.safe_agent_loop import SafeAgentLoop

def agent_status(request):
    return JsonResponse({
        "service": "master_agent_bridge",
        "status": "ready",
        "owner_approval_required": True,
    })

def execute_goal(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)
    try:
        body = json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"status": "error", "message": "invalid JSON"}, status=400)
    goal = str(body.get("goal", "")).strip()
    if not goal:
        return JsonResponse({"status": "error", "message": "goal required"}, status=400)
    result = SafeAgentLoop().execute_cycle(goal)
    return JsonResponse(result)
