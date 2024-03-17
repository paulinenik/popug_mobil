from celery import shared_task

from django.core.mail import send_mail
from django.db.models import Sum

from balance.models import Transaction
from balance.services.transaction_creator import TransactionCreator
from users.models import User


@shared_task(name="send_daily_payment_notification")
def send_daily_payment_notification(transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)

    send_mail(
        subject="Daily Payment",
        message=f"Hooray! You earned money today! This much: {transaction.absolute_amount}",
        recipient_list=[transaction.user.email],
    )


@shared_task(name="make_daily_payments")
def make_daily_payments():
    users = User.objects.filter()
    for user in users.iterator():
        balance = user.transactions.aggregate(balance=Sum("amount"))["balance"]
        if balance > 0:
            transaction = TransactionCreator(
                user=user,
                type=Transaction.Types.PAYMENT,
                amount=(balance * -1),
            )()
        send_daily_payment_notification.delay(transaction.pk)
