from django.urls import path

from .views import real_estate_home

app_name = "real_estate_portal"

urlpatterns = [
    path("", real_estate_home, name="home"),
]
