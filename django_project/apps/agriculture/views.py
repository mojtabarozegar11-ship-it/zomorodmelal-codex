from django.shortcuts import render

from .models import Farm, ProductionChain, ProductionProduct


def dashboard(request):
    return render(
        request,
        "agriculture/dashboard.html",
        {
            "farms": Farm.objects.filter(active=True)[:12],
            "products": ProductionProduct.objects.filter(active=True)[:20],
            "chains": ProductionChain.objects.filter(active=True)[:20],
        },
    )
