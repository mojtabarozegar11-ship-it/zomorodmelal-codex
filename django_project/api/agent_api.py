"""HTTP bridge between Django and the canonical approval-gated Master Agent."""
import json
from django.http import JsonResponse
from master_agent import MasterOrchestrator, MasterRuntime


def _master():
    return MasterOrchestrator(runtime=MasterRuntime())


def agent_status(request):
    return JsonResponse({
        "service": "master_agent_bridge",
        "status": "ready",
        "owner_approval_required": True,
        "engine": "master_agent",
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
    approved = bool(body.get("approved", False))
    result = _master().execute(goal, approved=approved)
    code = 202 if result["status"] == "approval_required" else 200
    return JsonResponse(result, status=code)
