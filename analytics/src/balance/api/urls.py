from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from balance.api.views.balance import BalanceView

router = SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("finance/", BalanceView.as_view(), name="finance-analytics"),
]
