"""HTTP bridge between Django and the safe Master Agent runtime."""
import json

from django.http import JsonResponse

from autonomous_core.safe_agent_loop import SafeAgentLoop


def _status_payload():
    return {
        "service": "master_agent_bridge",
        "status": "ready",
        "owner_approval_required": True,
        "execution": "approval_gated",
    }


def _endpoint_payload():
    return {
        "status": "ok",
        "version": "v1",
        "endpoints": {
            "status": "/api/v1/status/",
            "health": "/api/v1/health/",
            "execute": "/api/v1/agent/execute/",
        },
        "owner_approval_required": True,
    }


def agent_status(request):
    return JsonResponse({
        **_status_payload(),
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
    loop = SafeAgentLoop()
    result = loop.execute_cycle(goal)
    return JsonResponse(result)


def health(request):
    return JsonResponse({"status": "ok", "service": "django"})


def agent_dashboard(request):
    return JsonResponse({
        "service": "Zomorod Melal Master Agent",
        **_status_payload(),
        "owner": "مجتبی روزگار",
        "external_ai_enabled": False,
        "endpoints": {
            "status": "/api/status/",
            "health": "/api/health/",
            "execute": "/api/execute/",
            "v1": "/api/v1/",
        },
    })


def api_v1_status(request):
    return JsonResponse({**_status_payload(), **_endpoint_payload()})


def api_v1_health(request):
    return JsonResponse({
        "status": "ok",
        "service": "zomorod-melal-api",
        "version": "v1",
    })


def api_v1_execute(request):
    response = execute_goal(request)
    if response.status_code != 200:
        return response
    payload = json.loads(response.content.decode("utf-8"))
    payload["api_version"] = "v1"
    return JsonResponse(payload)


def api_v1_discovery(request):
    return JsonResponse({
        "service": "zomorod-melal-api",
        "version": "v1",
        "status": "ready",
        "owner_approval_required": True,
        "execution": "approval_gated",
        "endpoints": _endpoint_payload()["endpoints"],
    })
