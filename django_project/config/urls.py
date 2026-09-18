from django.contrib import admin
from django.urls import include, path

from apps.ai.mobile_admin import (
    mobile_admin,
    mobile_icon,
    mobile_manifest,
    mobile_service_worker,
)

urlpatterns = [
    path("", include("apps.site.urls")),
    path("", include("apps.economy.urls")),
    path("studio/", include("apps.studio.urls")),
    path("office/", include("apps.office.urls")),
    path("", include("apps.services.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/office/", include("apps.office.api_urls")),
    path("economy/", include("apps.economy.catalog_urls")),
    path("ai/", include("apps.ai.content_agent_urls")),
    path("mobile-admin/", mobile_admin, name="mobile-admin"),
    path(
        "mobile-admin/manifest.json",
        mobile_manifest,
        name="mobile-admin-manifest",
    ),
    path("mobile-admin/sw.js", mobile_service_worker, name="mobile-admin-sw"),
    path("mobile-admin/icon.svg", mobile_icon, name="mobile-admin-icon"),
]
