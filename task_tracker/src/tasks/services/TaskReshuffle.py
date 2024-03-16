from dataclasses import dataclass
from typing import Any

from app.services import BaseService
from tasks.models import Task
from tasks.services.TaskAssigner import TaskAssigner


class Producer:
    def call(self, *args: Any, **kwargs: Any) -> Any:
        pass


@dataclass
class TaskReshuffle(BaseService):
    def act(self) -> None:
        tasks = self.get_tasks()

        # TODO: Отправлять события батчем
        for task in tasks.iterator():
            TaskAssigner(task)()

    def get_tasks(self):
        return Task.objects.filter(status=Task.Statuses.IN_PROGRESS)
