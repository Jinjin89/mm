"""URL routing for the core app."""
from __future__ import annotations

from django.urls import path

from .views import HealthCheckView, ServiceOverviewView

urlpatterns = [
    path("", ServiceOverviewView.as_view(), name="api-root"),
    path("health/", HealthCheckView.as_view(), name="api-health"),
]
