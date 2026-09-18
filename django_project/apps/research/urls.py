from django.urls import path

from . import views

urlpatterns = [
    path("", views.research_home, name="research-home"),
    path("<int:project_id>/", views.research_project, name="research-project"),
]
