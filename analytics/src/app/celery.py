"""
https://docs.celeryproject.org/en/v4.4.7/django/first-steps-with-django.html
"""

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

__all__ = ["celery"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("analytics")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


celery.conf.beat_schedule = {
    "transactions-stream-polling": {
        "task": "transactions_stream_polling",
        "schedule": crontab(minute="*/1"),
        "options": {
            "expires": 60,
        },
    },
    "users-stream-polling": {
        "task": "users_stream_polling",
        "schedule": crontab(minute="*/1"),
        "options": {
            "expires": 60,
        },
    },
}
