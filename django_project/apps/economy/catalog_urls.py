from django.urls import path
from .catalog_views import catalog, catalog_api
urlpatterns=[path("services/", catalog, name="economy-service-catalog"), path("api/v1/services/", catalog_api, name="economy-service-catalog-api-v1")]
