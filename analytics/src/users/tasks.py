from celery import shared_task

from app.kafka.consumer import Consumer
from users.event_handlers import users_stream_event_handlers


@shared_task(name="users_stream_polling")
def users_stream_polling():
    Consumer(topic="users-stream", event_handlers=users_stream_event_handlers).run()
