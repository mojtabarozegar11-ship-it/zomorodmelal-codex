from django.urls import path
from . import views

urlpatterns = [path("", views.dashboard, name="office-dashboard"), path("app/", views.app_shell, name="office-app")]
