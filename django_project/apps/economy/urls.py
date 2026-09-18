from django.urls import path
from .views import dashboard, health

urlpatterns = [path("economy/", dashboard, name="economy-dashboard"), path("api/economy/health/", health, name="economy-health")]
