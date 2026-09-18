from django.urls import path
from . import views

urlpatterns = [
    path("architecture/", views.architecture_audit, name="architecture-audit"),
    path("", views.home, name="home"),
    path("page/<slug:slug>/", views.page_detail, name="page-detail"),
    path("encyclopedia/", views.encyclopedia, name="encyclopedia"),
    path("agriculture/weather/", views.agriculture_weather, name="agriculture-weather"),
    path("games/", views.studio_redirect, name="games"),
    path("health/", views.health, name="website-health"),
]
