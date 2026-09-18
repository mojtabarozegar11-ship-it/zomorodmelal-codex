"""HTTP bridge between Django and the safe Master Agent runtime."""
import json
from django.http import JsonResponse
from autonomous_core.safe_agent_loop import SafeAgentLoop
from autonomous_core.planner import Planner
from autonomous_core.executor import Executor
from autonomous_core.approval_gateway import ApprovalGateway


def agent_status(request):
    return JsonResponse({
        "service": "master_agent_bridge",
        "status": "ready",
        "owner_approval_required": True,
        "owner": "مجتبی روزگار",
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
    loop = SafeAgentLoop(Planner(), Executor(), ApprovalGateway())
    result = loop.execute_cycle(goal)
    return JsonResponse(result)


def health(request):
    return JsonResponse({"status": "ok", "service": "django"})


def agent_dashboard(request):
    return JsonResponse({
        "service": "Zomorod Melal Master Agent",
        "status": "ready",
        "execution": "approval_gated",
        "owner_approval_required": True,
        "owner": "مجتبی روزگار",
        "external_ai_enabled": False,
        "endpoints": {
            "status": "/api/status/",
            "health": "/api/health/",
            "execute": "/api/execute/",
        },
    })
