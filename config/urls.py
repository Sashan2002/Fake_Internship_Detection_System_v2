"""
Root URL configuration. Each Django app owns its own urls.py; this file
just mounts them under /api/.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/advertisements/", include("apps.advertisements.urls")),
    path("api/", include("apps.detection.urls")),
]
