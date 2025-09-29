"""Custom authentication backend using signed access tokens."""
from __future__ import annotations

from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from .tokens import InvalidToken, TokenExpired, verify_access_token

User = get_user_model()


class SignedTokenAuthentication(authentication.BaseAuthentication):
    """Authenticate requests using Bearer tokens issued by the API."""

    keyword = settings.AUTH_HEADER_TYPE

    def authenticate(self, request):  # type: ignore[override]
        header = authentication.get_authorization_header(request).split()
        if not header:
            return None

        if header[0].decode().lower() != self.keyword.lower():
            return None

        if len(header) == 1:
            raise exceptions.AuthenticationFailed("Invalid authorization header. No credentials provided.")
        if len(header) > 2:
            raise exceptions.AuthenticationFailed("Invalid authorization header. Credentials string should not contain spaces.")

        token = header[1].decode()
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token: str):
        try:
            payload = verify_access_token(token)
        except TokenExpired as exc:
            raise exceptions.AuthenticationFailed(str(exc)) from exc
        except InvalidToken as exc:
            raise exceptions.AuthenticationFailed(str(exc)) from exc

        user_id: Optional[int] = payload.get("uid") if isinstance(payload, dict) else None
        if user_id is None:
            raise exceptions.AuthenticationFailed("Token payload missing user id.")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("User not found.") from exc

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User account is disabled.")

        return (user, None)
