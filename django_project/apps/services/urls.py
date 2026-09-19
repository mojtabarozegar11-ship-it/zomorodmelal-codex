from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="services"),
    path("<slug:slug>/", views.detail, name="service-detail"),
    path("<slug:slug>/request/", views.request_service, name="service-request"),
    path("requests/<str:tracking_code>/", views.request_detail, name="service-request-detail"),
]
