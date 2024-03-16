from dataclasses import dataclass
import random
from typing import Any

from django.db.models import Q

from app.kafka.producer import Producer
from app.services import BaseService
from users.models import User


@dataclass
class TaskAssigner(BaseService):
    instance: "Task"

    def act(self) -> None:
        self.instance.assignee = self.get_random_user()
        self.instance.save()
        self.produce_business_event()

    def get_random_user(self) -> "User":
        developers = User.objects.filter(~Q(role__in=[User.Roles.ADMIN, User.Roles.MANAGER]))
        return random.choice(developers)

    def produce_business_event(self) -> None:
        Producer(event="TaskAssigned", topic="tasks-lifecycle", data={"task_id": self.instance.public_id, "assignee_id": self.instance.assignee.public_id})
