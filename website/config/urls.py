from django.urls import path
from website.core.views import home, page_detail, health

urlpatterns = [
    path("", home, name="home"),
    path("page/<slug:slug>/", page_detail, name="page-detail"),
    path("health/", health, name="website-health"),
]
