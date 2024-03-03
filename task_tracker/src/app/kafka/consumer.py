import json
import sys
import threading

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException


def create_user(data):
    from users.models import User

    user = User.objects.create(**data)
    print(f"User {user.username} {data} created")


class Consumer(threading.Thread):

    def __init__(self, event_handler, topic):
        super().__init__()
        self.event_handler = event_handler
        self.topic = topic

        if not callable(self.event_handler):
            raise ValueError("event_handler must be a callable")

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
                    self.event_handler(data)
        finally:
            self.consumer.close()
            print("Consumer closed")
