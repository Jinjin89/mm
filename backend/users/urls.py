"""Routing for user management endpoints."""
from __future__ import annotations

from django.urls import path

from .views import LoginView, RefreshTokenView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
]
