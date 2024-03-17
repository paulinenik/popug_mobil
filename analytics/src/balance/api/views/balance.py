from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from balance.services.finance_analytics import FinanceAnalytics
from users.api.permissions import AdminPermission


class BalanceView(APIView):
    permission_classes = [AdminPermission]

    def get(self, request: "Request", *args: Any, **kwargs: Any) -> "Response":
        return Response(FinanceAnalytics()(), status=200)
