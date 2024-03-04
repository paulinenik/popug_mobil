from dataclasses import dataclass
import random
from typing import Any

from django.db.models import Q

from app.services import BaseService
from users.models import User


class Producer:
    def call(self, *args: Any, **kwargs: Any) -> Any:
        pass


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
        Producer().call("TaskAssigned", topic="tasks")
