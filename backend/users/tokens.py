"""Utility helpers to issue and validate signed tokens."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from django.conf import settings
from django.core import signing

ACCESS_SALT = "users.access"
REFRESH_SALT = "users.refresh"


class TokenError(Exception):
    """Base exception for token issues."""


class TokenExpired(TokenError):
    """Raised when a token is expired."""


class InvalidToken(TokenError):
    """Raised when a token cannot be validated."""


@dataclass(slots=True)
class TokenPair:
    """Simple container for access and refresh tokens."""

    access: str
    refresh: str
    user_id: int


def _get_max_age(delta) -> int:
    return int(delta.total_seconds())


def issue_token_pair(user_id: int) -> TokenPair:
    """Create a signed access/refresh token pair for the given user id."""

    access_token = signing.dumps({"uid": user_id, "type": "access"}, salt=ACCESS_SALT)
    refresh_token = signing.dumps({"uid": user_id, "type": "refresh"}, salt=REFRESH_SALT)
    return TokenPair(access=access_token, refresh=refresh_token, user_id=user_id)


def verify_access_token(token: str) -> Dict[str, Any]:
    """Validate an access token and return its payload."""

    try:
        return signing.loads(
            token,
            salt=ACCESS_SALT,
            max_age=_get_max_age(settings.ACCESS_TOKEN_LIFETIME),
        )
    except signing.SignatureExpired as exc:  # pragma: no cover - defensive
        raise TokenExpired("Access token has expired") from exc
    except signing.BadSignature as exc:  # pragma: no cover - defensive
        raise InvalidToken("Access token is invalid") from exc


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Validate a refresh token and return its payload."""

    try:
        return signing.loads(
            token,
            salt=REFRESH_SALT,
            max_age=_get_max_age(settings.REFRESH_TOKEN_LIFETIME),
        )
    except signing.SignatureExpired as exc:  # pragma: no cover - defensive
        raise TokenExpired("Refresh token has expired") from exc
    except signing.BadSignature as exc:  # pragma: no cover - defensive
        raise InvalidToken("Refresh token is invalid") from exc


def rotate_refresh_token(refresh_token: str) -> TokenPair:
    """Validate a refresh token and issue a new token pair."""

    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("uid")
    if user_id is None:
        raise InvalidToken("Refresh token payload missing user id")
    return issue_token_pair(int(user_id))
