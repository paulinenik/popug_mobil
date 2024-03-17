from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db.models import F
from django.db.models import Sum

from app.services import BaseService
from balance.models.transaction import Transaction

if TYPE_CHECKING:
    from users.models import User


@dataclass
class BalancePerWeek(BaseService):
    user: "User"

    def act(self) -> dict:
        transactions = self._get_transaction_for_last_week()
        return {
            "current": self._get_current_balance(),
            "income_per_day": transactions.annotate(date=F("created_at__date")).values("date").annotate(amount=Sum("amount")),
        }

    def _get_transaction_for_last_week(self):
        return Transaction.objects.filter(user=self.user, created_at__date__gte=self._get_last_week_start_date()).exclude(type=Transaction.Types.PAYMENT)

    def _get_last_week_start_date(self) -> datetime.date:
        return datetime.now().date() - timedelta(days=7)

    def _get_current_balance(self) -> int:
        return self.user.transactions.aggregate(balance=Sum("amount"))["balance"]
