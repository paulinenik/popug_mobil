from rest_framework.permissions import IsAuthenticated

from app.api.viewsets import ReadonlyModelViewSet
from balance.api.serializers.transaction import TransactionSerializer
from balance.models import Transaction
from users.models import User


class TransactionsViewSet(ReadonlyModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role not in [User.Roles.ADMIN, User.Roles.MANAGER]:
            return self.queryset.filter(user=self.request.user)
        return self.queryset
