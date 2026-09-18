from django.urls import path
from .catalog_views import catalog
urlpatterns=[path("services/", catalog, name="economy-service-catalog")]
