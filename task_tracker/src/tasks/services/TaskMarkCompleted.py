from dataclasses import dataclass
from typing import Any

from app.services import BaseService


class Producer:
    def call(self, *args: Any, **kwargs: Any) -> Any:
        pass


@dataclass
class TaskMarkCompleted(BaseService):
    instance: "Task"

    def act(self) -> None:
        self.instance.status = self.instance.Statuses.DONE
        self.instance.save()
        self.produce_business_event()

    def produce_business_event(self) -> None:
        Producer().call("TaskCompleted", topic="tasks")
