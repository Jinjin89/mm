"""Views for the core app."""
from __future__ import annotations

from datetime import datetime

from django.conf import settings
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
