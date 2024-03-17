from balance.services.transaction_creator import TransactionCreator
from tasks.models.task import Task
from users.models import User


def task_assigned_event_handler(data):
    assignee, _ = User.objects.get_or_create(public_id=data["assignee_id"])
    task, _ = Task.objects.update_or_create(
        public_id=data["task_id"],
        defaults={"assignee": assignee},
    )
    TransactionCreator(
        user=assignee,
        type=task.Types.TASK_FEE,
        amount=(task.fee * -1),
    )()


def task_completed_event_handler(data):
    assignee, _ = User.objects.get_or_create(public_id=data["assignee_id"])
    task, _ = Task.objects.update_or_create(
        public_id=data["task_id"],
        defaults={
            "status": Task.Statuses.DONE,
            "assignee": assignee,
        },
    )
    TransactionCreator(
        user=assignee,
        type=task.Types.TASK_REWARD,
        amount=task.reward,
    )()


tasks_lifecycle_event_handlers = {
    "TaskAssigned": task_assigned_event_handler,
    "TaskCompleted": task_completed_event_handler,
}
