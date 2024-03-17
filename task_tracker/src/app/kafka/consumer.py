import json
import sys
import threading
from typing import Callable

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException


def create_user(data):
    from users.models import User

    user = User.objects.create(**data)
    print(f"User {user.username} {data} created")


class Consumer(threading.Thread):

    def __init__(self, event_handlers: dict[str, Callable], topic: str):
        super().__init__()
        self.event_handlers = event_handlers
        self.topic = topic

        if not isinstance(self.event_handlers, dict):
            raise ValueError("event_handler must be a dict")

        conf = {"bootstrap.servers": "localhost:9092", "auto.offset.reset": "smallest", "group.id": "user_group"}
        self.consumer = KafkaConsumer(conf)

    def run(self):
        running = True
        try:
            self.consumer.subscribe([self.topic])
            while running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    break
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write("%% %s [%d] reached end at offset %d\n" % (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value().decode("utf-8"))
                    key = msg.key()  # Get the key associated with the message
                    self._get_event_handler(key)(data)
        finally:
            self.consumer.close()
            print("Consumer closed")

    def _get_event_handler(self, key: str) -> Callable:
        event_handler = self.event_handlers.get(key)
        if not event_handler:
            raise ValueError(f"No event handler found for event {key}")
        if not callable(event_handler):
            raise ValueError(f"Event handler for event {key} is not callable")
        return event_handler
