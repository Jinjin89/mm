"""Celery application for the music platform."""
from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_platform.settings")

app = Celery("music_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self) -> str:
    """Default debug task to verify Celery configuration."""
    return f"Request: {self.request!r}"
