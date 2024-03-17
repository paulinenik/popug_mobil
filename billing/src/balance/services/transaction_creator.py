from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.kafka.producer import Producer
from app.services import BaseService
from balance.models.transaction import Transaction

if TYPE_CHECKING:
    from users.models import User


@dataclass
class TransactionCreator(BaseService):
    user: "User"
    type: str
    amount: int
    task: "Task | None" = None

    def act(self) -> "Transaction":
        return Transaction.objects.create(user=self.user, type=self.type, amount=self.amount, task=self.task)

    def _create_transaction(self) -> "Transaction":
        return Transaction.objects.create(user=self.user, type=self.type, amount=self.amount, task=self.task)

    def _produce_event(self) -> None:
        Producer(topic="transactions-stream", event="TransactionCreated", data=self._get_event_data())()

    def _get_event_data(self) -> dict:
        data = {
            "user_id": self.user.public_id,
            "type": self.type,
            "amount": self.amount,
        }
        if self.task:
            data["task_id"] = self.task.public_id
        return data
