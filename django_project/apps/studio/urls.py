from django.urls import path

from . import views

urlpatterns = [path("", views.studio_home, name="studio-home")]
