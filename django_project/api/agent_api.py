"""Canonical HTTP API for the unified Site -> Master -> Worker runtime."""
from __future__ import annotations

import json

from django.http import JsonResponse

from django_integration.agent_service import AgentService

service = AgentService()


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        return None


def agent_status(request):
    return JsonResponse({
        "service": "zomorodmelal-unified-runtime",
        "status": "ready",
        "architecture": "site -> master -> worker -> execution -> result",
        "approval_required": True,
    })


def execute_goal(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=405)
    body = _json_body(request)
    if body is None:
        return JsonResponse({"status": "error", "message": "invalid JSON"}, status=400)
    goal = str(body.get("goal", "")).strip()
    if not goal:
        return JsonResponse({"status": "error", "message": "goal required"}, status=400)
    context = body.get("context") or {}
    if not isinstance(context, dict):
        return JsonResponse({"status": "error", "message": "context must be an object"}, status=400)
    approved = bool(body.get("approved", False))
    return JsonResponse(service.run(goal, context=context, approved=approved))


def health(request):
    return JsonResponse({"status": "ok", "service": "django"})


def agent_dashboard(request):
    return JsonResponse({
        "service": "Zomorod Melal Unified Runtime",
        "status": "ready",
        "architecture": "site -> master -> worker -> execution -> result",
        "approval_gated": True,
        "endpoints": {
            "status": "/api/status/",
            "health": "/api/health/",
            "execute": "/api/execute/",
            "worker_health": "/api/worker-health/",
        },
    })
