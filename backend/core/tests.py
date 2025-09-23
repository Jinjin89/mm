"""Tests for the core app."""
from __future__ import annotations

from django.test import TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    """Basic tests covering the health endpoint."""

    def test_health_endpoint_returns_ok_status(self) -> None:
        response = self.client.get(reverse("api-health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
