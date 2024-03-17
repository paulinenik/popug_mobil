from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from balance.api.views.balance import BalanceView
from balance.api.views.transaction import TransactionsViewSet

router = SimpleRouter()
router.register("transactions", TransactionsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", BalanceView.as_view(), name="balance"),
]
