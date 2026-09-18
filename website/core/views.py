from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import SitePage


def home(request):
    return render(request, "home.html")


def page_detail(request, slug):
    page = get_object_or_404(SitePage, slug=slug, published=True)
    return render(request, "company.html", {"page": page})


def health(request):
    return JsonResponse({"status": "ok", "service": "Zomorod Melal Website Core"})
