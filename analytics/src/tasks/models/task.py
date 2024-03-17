from django.db import models

from app.models import DefaultModel


class Task(DefaultModel):
    public_id = models.UUIDField(unique=True)
