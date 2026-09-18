from django.urls import path

from . import views

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("<slug:slug>/", views.product_detail, name="marketplace-product"),
]
