"""Tests for the users API."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    """Ensure the registration and login flows behave as expected."""

    def test_register_user_with_email(self):
        payload = {
            "email": "listener@example.com",
            "phone_number": "",
            "full_name": "Demo Listener",
            "password": "Supersafe123",
            "confirm_password": "Supersafe123",
        }

        response = self.client.post(reverse("auth-register"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertTrue(User.objects.filter(email="listener@example.com").exists())

    def test_login_with_email(self):
        user = User.objects.create_user(email="dj@example.com", password="Supersafe123")

        response = self.client.post(
            reverse("auth-login"),
            {"identifier": "dj@example.com", "password": "Supersafe123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["id"], user.id)
        self.assertIn("access", response.data["tokens"])

    def test_login_with_phone(self):
        user = User.objects.create_user(phone_number="13800138000", password="Supersafe123")

        response = self.client.post(
            reverse("auth-login"),
            {"identifier": "13800138000", "password": "Supersafe123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["id"], user.id)
        self.assertIn("refresh", response.data["tokens"])

    def test_refresh_token(self):
        user = User.objects.create_user(email="refresh@example.com", password="Supersafe123")
        login_response = self.client.post(
            reverse("auth-login"),
            {"identifier": "refresh@example.com", "password": "Supersafe123"},
            format="json",
        )
        refresh_token = login_response.data["tokens"]["refresh"]

        response = self.client.post(reverse("auth-refresh"), {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])
        self.assertEqual(response.data["user"]["id"], user.id)

    def test_register_requires_matching_passwords(self):
        payload = {
            "email": "mismatch@example.com",
            "password": "Supersafe123",
            "confirm_password": "Different123",
        }
        response = self.client.post(reverse("auth-register"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", response.data)
