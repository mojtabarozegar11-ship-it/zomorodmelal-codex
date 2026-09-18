from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("page/<slug:slug>/", views.page_detail, name="page-detail"),
    path("encyclopedia/", views.encyclopedia, name="encyclopedia"),
    path("health/", views.health, name="website-health"),
]
