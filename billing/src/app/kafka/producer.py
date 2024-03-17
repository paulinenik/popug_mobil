from dataclasses import dataclass
import json
import socket

from confluent_kafka import Producer as KafkaProducer

from app.services import BaseService


@dataclass
class Producer(BaseService):
    event: str
    topic: str
    data: dict

    @property
    def producer(self):
        conf = {"bootstrap.servers": "localhost:9092", "client.id": socket.gethostname()}
        return KafkaProducer(conf)

    def act(self):
        print(f"Sending to Kafka: topic: {self.topic}, key: {self.event}, body: {self.data}")
        self.producer.produce(topic=self.topic, key=self.event, value=json.dumps(self.data))
        self.producer.flush()
