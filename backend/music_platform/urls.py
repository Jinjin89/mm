"""URL configuration for the music platform project."""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

from core.views import ServiceOverviewView

urlpatterns = [
    path("", ServiceOverviewView.as_view(), name="service-overview"),
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
