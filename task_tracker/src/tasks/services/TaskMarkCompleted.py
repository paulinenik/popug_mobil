from dataclasses import dataclass
from typing import Any

from app.kafka.producer import Producer
from app.services import BaseService
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tasks.models import Task


@dataclass
class TaskMarkCompleted(BaseService):
    instance: "Task"

    def act(self) -> None:
        self.instance.status = self.instance.Statuses.DONE
        self.instance.save()
        self.produce_business_event()

    def produce_business_event(self) -> None:
        Producer(event="TaskCompleted", topic="tasks-lifecycle", data={"task_id": self.instance.public_id, "assignee_id": self.instance.assignee.public_id})()
