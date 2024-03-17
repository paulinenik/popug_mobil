from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from django.db.models import QuerySet
from django.db.models import Sum

from app.services import BaseService
from balance.models.transaction import Transaction


@dataclass
class ManagerIncomePerWeek(BaseService):
    @property
    def today(self) -> datetime.date:
        return timezone.now().date()

    def act(self) -> dict:
        return {
            "today": self._get_today_income(),
            "income_per_day": self._get_income_for_last_week(),
        }

    def _get_today_income(self) -> int:
        return self._get_balance(self._get_transactions_for_date(self.today))

    def _get_income_for_last_week(self) -> dict:
        result = {}
        for i in range(7):
            date = self.today - timedelta(days=i)
            result[date] = self._get_balance(self._get_transactions_for_date(date))
        return result

    def _get_transactions_for_date(self, date) -> "QuerySet[Transaction]":
        return Transaction.objects.filter(created_at__date=date)

    def _get_balance(self, transactions: "QuerySet[Transaction]") -> int:
        return (
            transactions.filter(type=Transaction.Types.TASK_FEE).aggregate(amount=Sum("amount"))["amount"]
            - transactions.filter(type=Transaction.Types.TASK_REWARD).aggregate(amount=Sum("amount"))["amount"]
        )
