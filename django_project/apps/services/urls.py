from django.urls import path
from . import views

urlpatterns = [
    path("services/", views.index, name="services"),
    path("services/<slug:slug>/", views.detail, name="service-detail"),
    path("services/<slug:slug>/request/", views.request_service, name="service-request"),
    path("services/requests/<str:tracking_code>/", views.request_detail, name="service-request-detail"),
]
