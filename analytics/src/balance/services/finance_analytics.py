from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta

from django.db.models import QuerySet
from django.db.models import Sum
from django.utils import timezone

from app.services import BaseService
from balance.models.transaction import Transaction
from users.models import User


@dataclass
class FinanceAnalytics(BaseService):
    @property
    def today(self) -> datetime.date:
        return timezone.now().date()

    def act(self) -> dict:
        return {
            "today": self._get_today_income(),
            "bankrupted_today": self._get_bankrupted_today(),
            "most_expensive_task_today": self._get_most_expensive_task("today"),
            "most_expensive_task_this_week": self._get_most_expensive_task("week"),
            "most_expensive_task_this_month": self._get_most_expensive_task("month"),
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

    def _get_bankrupted_today(self) -> int:
        return User.objects.annotate(balance=Sum("transactions__amount")).filter(balance__lt=0).count()

    def _get_most_expensive_task(self, period: "str") -> "int | None":
        if period == "today":
            filter_args = {"created_at__date": self.today}
        elif period == "week":
            filter_args = {"created_at__gte": self.today - timedelta(days=7)}
        elif period == "month":
            filter_args = {"created_at__gte": self.today - timedelta(days=30)}
        else:
            raise ValueError(f"Invalid period: {period}")

        transaction = Transaction.objects.filter(**filter_args).filter(type=Transaction.Types.TASK_REWARD).order_by("amount").first()
        return transaction.amount if transaction else None
