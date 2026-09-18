from django.shortcuts import render
from .service_catalog import SERVICE_CATALOG

def catalog(request):
    return render(request, "economy/service_catalog.html", {"catalog": SERVICE_CATALOG})


def catalog_api(request):
    from django.http import JsonResponse
    from .service_catalog import SERVICE_CATALOG
    return JsonResponse({"version":"v1","services":SERVICE_CATALOG})
