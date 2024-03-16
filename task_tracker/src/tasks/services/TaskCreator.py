from dataclasses import dataclass
from typing import Any

from app.kafka.producer import Producer
from app.services import BaseService
from tasks.models import Task
from tasks.services.TaskAssigner import TaskAssigner
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tasks.models import Task


@dataclass
class TaskCreator(BaseService):
    data: dict

    def act(self) -> None:
        task = Task.objects.create(**self.data)
        self.produce_cud_event(task)
        TaskAssigner(task)()

    def produce_cud_event(self, task: "Task") -> None:
        Producer(event="TaskCreated", topic="tasks-stream", data={"task_id": task.public_id, "status": task.status, **self.data})()
