"""Unified management status for Site, Master Agent and Worker Mojtaba."""
from __future__ import annotations
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_integration.agent_bridge import AgentBridge

@login_required
def unified_status(request):
    if not request.user.is_staff:
        return JsonResponse({"status": "forbidden"}, status=403)
    worker = AgentBridge().health()
    return JsonResponse({
        "status": "ready",
        "panels": {
            "site": {"name": "سایت", "status": "ready", "health": "/api/health/", "dashboard": "/"},
            "master": {"name": "Master Agent", "status": "ready", "approval_gated": True, "dashboard": "/api/dashboard/"},
            "worker": {"name": "کارگر مجتبی", "status": worker.get("status", "unknown"), "health": worker},
        },
        "architecture": "site -> master -> worker",
        "android": {"installable": True, "mode": "PWA", "path": "/mobile-admin/"},
    })
