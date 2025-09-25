"""Views for the core app."""
from __future__ import annotations

from datetime import datetime

from django.conf import settings
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Simple API view to ensure the stack is operational."""

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request, *args, **kwargs):  # type: ignore[override]
        return Response(
            {
                "status": "ok",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "environment": {
                    "debug": settings.DEBUG,
                    "database": settings.DATABASES["default"]["HOST"],
                    "redis": settings.CELERY_BROKER_URL,
                    "minio": settings.MINIO_ENDPOINT,
                },
            }
        )


class ServiceOverviewView(APIView):
    """Provide a small JSON landing page for the service."""

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request: Request, *args, **kwargs):  # type: ignore[override]
        health_url = request.build_absolute_uri(reverse("api-health"))
        api_root_url = request.build_absolute_uri(reverse("api-root"))
        admin_url = request.build_absolute_uri(reverse("admin:index"))

        return Response(
            {
                "service": "Music Platform API",
                "message": "Welcome to the self-hosted music platform backend.",
                "links": {
                    "api_root": api_root_url,
                    "health": health_url,
                    "admin": admin_url,
                },
            }
        )
