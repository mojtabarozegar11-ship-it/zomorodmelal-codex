from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import SitePage

def home(request): return render(request, "site/home.html")
def page_detail(request, slug):
    page = get_object_or_404(SitePage, slug=slug, published=True)
    return render(request, "site/page_detail.html", {"page": page})
def encyclopedia(request): return render(request, "site/encyclopedia.html")
def health(request): return JsonResponse({"status":"ok","service":"Zomorod Melal Website"})
