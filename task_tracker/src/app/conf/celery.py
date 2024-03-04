from app.conf.environ import env
from app.conf.timezone import TIME_ZONE

CELERY_BROKER_URL = env("CELERY_BROKER_URL", cast=str, default="redis://localhost:6380/0")
CELERY_TASK_ALWAYS_EAGER = env(
    "CELERY_TASK_ALWAYS_EAGER", cast=bool, default=env("DEBUG")
)  # https://docs.celeryproject.org/en/v4.4.7/userguide/configuration.html#std:setting-task_always_eager
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_TASK_DEFAULT_QUEUE = "task_tracker_celery"
