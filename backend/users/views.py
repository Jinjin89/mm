"""Views for user registration and authentication."""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer
from .tokens import InvalidToken, TokenExpired, issue_token_pair, rotate_refresh_token

User = get_user_model()


class RegisterView(APIView):
    """Create a new user account and return JWT tokens."""

    authentication_classes: list = []
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):  # type: ignore[override]
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = issue_token_pair(user.id)
        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {"refresh": tokens.refresh, "access": tokens.access},
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate with email or phone number and return JWT tokens."""

    authentication_classes: list = []
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):  # type: ignore[override]
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"detail": _("Both identifier and password are required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = (
            User.objects.filter(Q(email__iexact=identifier) | Q(phone_number=identifier))
            .distinct()
            .first()
        )

        if user is None or not user.check_password(password):
            return Response(
                {"detail": _("Unable to log in with provided credentials.")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response({"detail": _("User account is disabled.")}, status=status.HTTP_403_FORBIDDEN)

        tokens = issue_token_pair(user.id)
        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {"refresh": tokens.refresh, "access": tokens.access},
            }
        )


class RefreshTokenView(APIView):
    """Exchange a refresh token for a new token pair."""

    authentication_classes: list = []
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):  # type: ignore[override]
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": _("Refresh token is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tokens = rotate_refresh_token(refresh_token)
        except TokenExpired as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=tokens.user_id)

        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": {"refresh": tokens.refresh, "access": tokens.access},
            }
        )
