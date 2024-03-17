from django.db import models
from django.db.models.enums import TextChoices

from app.models import TimestampedModel


class Transaction(TimestampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="transactions")
    task = models.ForeignKey("tasks.Task", on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)
    amount = models.IntegerField()

    class Types(TextChoices):
        TASK_FEE = "task_fee", "Task Fee"
        TASK_REWARD = "task_reward", "Task Reward"
        PAYMENT = "payment", "Payment"

    type = models.CharField(choices=Types.choices, max_length=32)

    @property
    def absolute_amount(self):
        return abs(self.amount)
