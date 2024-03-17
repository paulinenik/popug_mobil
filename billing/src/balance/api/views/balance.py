from typing import Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from balance.services.balance_per_week import BalancePerWeek
from balance.services.manager_income_per_week import ManagerIncomePerWeek
from users.models import User


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: "Request", *args: Any, **kwargs: Any) -> "Response":
        if request.user.role in [User.Roles.ADMIN, User.Roles.MANAGER]:  # type: ignore
            return Response(ManagerIncomePerWeek()(), status=200)
        return Response(BalancePerWeek(request.user)(), status=200)  # type: ignore
