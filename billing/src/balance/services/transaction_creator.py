from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.services import BaseService
from balance.models.transaction import Transaction

if TYPE_CHECKING:
    from users.models import User


@dataclass
class TransactionCreator(BaseService):
    user: "User"
    type: str
    amount: int

    def act(self) -> "Transaction":
        return Transaction.objects.create(user=self.user, type=self.type, amount=self.amount)
