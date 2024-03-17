from tasks.models.task import Task


def task_created_event_handler(data):
    public_id = data.pop("public_id")
    Task.objects.update_or_create(
        public_id=public_id,
        defaults=data,
    )


tasks_stream_event_handlers = {
    "TaskCreated": task_created_event_handler,
}
