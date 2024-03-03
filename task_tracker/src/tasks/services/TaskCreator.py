from dataclasses import dataclass
from typing import Any

from app.services import BaseService
from tasks.models import Task
from tasks.services.TaskAssigner import TaskAssigner


class Producer:
    def call(self, *args: Any, **kwargs: Any) -> Any:
        pass


@dataclass
class TaskCreator(BaseService):
    data: dict

    def act(self) -> None:
        task = Task.objects.create(**self.data)
        self.produce_cud_event()
        TaskAssigner(task)()

    def produce_cud_event(self) -> None:
        Producer().call("TaskCreated", topic="tasks-stream")
