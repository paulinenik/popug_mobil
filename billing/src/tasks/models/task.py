import random

from django.db import models
from django.db.models import TextChoices

from app.models import DefaultModel


def generate_task_fee():
    return random.randint(10, 20)


def generate_task_reward():
    return random.randint(20, 40)


class Task(DefaultModel):
    created = models.DateTimeField(blank=True, null=True, db_index=True)
    modified = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)

    class Statuses(TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    status = models.CharField(choices=Statuses.choices, max_length=32, default=Statuses.IN_PROGRESS)
    assignee = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="tasks", blank=True)
    public_id = models.UUIDField(unique=True)
    fee = models.IntegerField(default=generate_task_fee)
    reward = models.IntegerField(default=generate_task_reward)
