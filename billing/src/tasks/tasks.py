from celery import shared_task

from app.kafka.consumer import Consumer
from tasks.event_handlers.tasks_lifecycle import tasks_lifecycle_event_handlers
from tasks.event_handlers.tasks_stream import tasks_stream_event_handlers


@shared_task(name="tasks_stream_polling")
def tasks_stream_polling():
    Consumer(topic="tasks-stream", event_handlers=tasks_stream_event_handlers).run()


@shared_task(name="tasks_lifecycle_polling")
def tasks_lifecycle_polling():
    Consumer(topic="tasks-lifecycle", event_handlers=tasks_lifecycle_event_handlers).run()
