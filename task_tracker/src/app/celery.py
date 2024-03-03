"""
https://docs.celeryproject.org/en/v4.4.7/django/first-steps-with-django.html
"""

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

__all__ = ["celery"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

celery = Celery("task_tracker")
celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


celery.conf.beat_schedule = {
    "deactivate-subscriptions": {
        "task": "deactivate_subscriptions",
        "schedule": crontab(hour="0", minute="0"),
        "options": {
            "expires": 600,
        },
    },
    "notify-about-reminder": {
        "task": "notify_about_reminder",
        "schedule": crontab(minute="*/1"),
        "options": {
            "expires": 600,
        },
    },
    "notify-owners-about_yesterday-stat": {
        "task": "notify_owners_about_yesterday_stat",
        "schedule": crontab(hour="8", minute="0"),
        "options": {
            "expires": 600,
        },
    },
    "update-active-subscriptions-in-google-wallet": {
        "task": "update_active_subscriptions_in_google_wallet",
        "schedule": crontab(hour="0", minute="0"),
        "options": {
            "expires": 600,
        },
    },
    "expire-gifts": {
        "task": "expire_gifts",
        "schedule": crontab(minute="*/1"),
        "options": {
            "expires": 600,
        },
    },
}
