from django.shortcuts import render
from .service_catalog import SERVICE_CATALOG

def catalog(request):
    return render(request, "economy/service_catalog.html", {"catalog": SERVICE_CATALOG})
