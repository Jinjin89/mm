"""Celery tasks for the core app."""
from __future__ import annotations

from celery import shared_task


@shared_task
def ping() -> str:
    """Simple task used to verify Celery workers are running."""
    return "pong"
