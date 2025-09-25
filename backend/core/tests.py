"""Tests for the core app."""
from __future__ import annotations

from django.test import TestCase
from django.urls import reverse


class TestHealthEndpoint(TestCase):
    """Basic tests covering the health endpoint."""

    def test_health_endpoint_returns_ok_status(self) -> None:
        response = self.client.get(reverse("api-health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


class TestServiceOverview(TestCase):
    """Ensure the landing page renders useful metadata."""

    def test_root_path_returns_overview_payload(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["service"], "Music Platform API")
        self.assertIn("links", payload)
        self.assertIn("api_root", payload["links"])
        self.assertIn("health", payload["links"])

    def test_api_root_matches_top_level_response(self) -> None:
        top_level_response = self.client.get("/")
        self.assertEqual(top_level_response.status_code, 200)

        api_root_response = self.client.get(reverse("api-root"))
        self.assertEqual(api_root_response.status_code, 200)
        self.assertEqual(api_root_response.json(), top_level_response.json())
