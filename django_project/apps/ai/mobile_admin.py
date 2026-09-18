from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import AIConfiguration

@login_required
def mobile_admin(request):
    if not request.user.is_staff:
        return redirect(reverse("admin:login") + "?next=" + reverse("mobile-admin"))
    config = AIConfiguration.objects.filter(provider="deepseek").first()
    context = {
        "ai_enabled": bool(config and config.enabled),
        "ai_configured": bool(config and config.api_key),
        "admin_url": reverse("admin:index"),
        "ai_url": reverse("admin:apps_ai_aiconfiguration_changelist"),
    }
    return render(request, "ai/mobile_admin.html", context)

def mobile_manifest(request):
    return JsonResponse({
        "name": "Zomorod Melal Admin",
        "short_name": "Zomorod Admin",
        "start_url": "/mobile-admin/",
        "scope": "/mobile-admin/",
        "display": "standalone",
        "orientation": "portrait",
        "lang": "fa",
        "dir": "rtl",
        "theme_color": "#0f5132",
        "background_color": "#ffffff",
        "icons": [{"src": "/mobile-admin/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
    })

def mobile_service_worker(request):
    script = """const CACHE="zomorod-admin-v1";
self.addEventListener("install",event=>{event.waitUntil(caches.open(CACHE).then(c=>c.add("/mobile-admin/")));self.skipWaiting();});
self.addEventListener("activate",event=>event.waitUntil(self.clients.claim()));
self.addEventListener("fetch",event=>{if(event.request.method!=="GET")return;event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));});
"""
    return HttpResponse(script, content_type="application/javascript")

def mobile_icon(request):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" rx="40" fill="#0f5132"/><circle cx="96" cy="96" r="62" fill="#fff"/><path d="M96 45c-28 22-45 39-45 65 0 25 20 45 45 45s45-20 45-45c0-26-17-43-45-65z" fill="#198754"/><path d="M96 73c-11 12-18 22-18 35 0 10 8 18 18 18s18-8 18-18c0-13-7-23-18-35z" fill="#d4af37"/></svg>"""
    return HttpResponse(svg, content_type="image/svg+xml")
