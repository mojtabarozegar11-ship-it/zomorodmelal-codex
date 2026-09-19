from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, redirect, render
from .models import SitePage

def home(request):
    return render(
        request,
        "site/home.html",
        {
            "quick_links": [
                ("کشاورزی", "agriculture-dashboard", "مزارع، محصولات و زنجیره‌های تولید"),
                ("بازار", "marketplace", "کاتالوگ محصولات و عرضه"),
                ("پژوهش", "research-home", "پروژه‌ها و توسعه دانش"),
                ("خدمات", "services", "خدمات و ثبت درخواست"),
                ("اقتصاد", "economy-dashboard", "اقتصاد و تحلیل"),
                ("استودیو", "studio-home", "بازی، اپلیکیشن و نوآوری"),
            ]
        },
    )

def page_detail(request, slug):
    page = get_object_or_404(SitePage, slug=slug, published=True)
    return render(request, "site/page_detail.html", {"page": page})

def encyclopedia(request):
    return render(request, "site/encyclopedia.html")

def agriculture_weather(request):
    return render(request, "site/agriculture_weather.html")

def health(request):
    return JsonResponse({"status": "ok", "service": "Zomorod Melal Website"})

def studio_redirect(request):
    return redirect("studio-home")


def architecture_audit(request):
    return JsonResponse({"status": "ok", "service": "architecture", "message": "Architecture audit endpoint is available."})


@require_GET
def api_status(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "zomorod-melal-site",
            "version": "1.0",
            "modules": [
                "agriculture",
                "marketplace",
                "research",
                "services",
                "economy",
                "studio",
                "ai",
                "office",
            ],
        }
    )
