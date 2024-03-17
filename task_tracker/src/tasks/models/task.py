import uuid

from django.db import models
from django.db.models import TextChoices

from app.models import TimestampedModel


class Task(TimestampedModel):
    title = models.CharField(max_length=255)

    class Statuses(TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    status = models.CharField(choices=Statuses.choices, max_length=32, default=Statuses.IN_PROGRESS)
    assignee = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tasks")
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
