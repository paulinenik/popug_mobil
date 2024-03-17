from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from balance.api import viewsets

router = SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
]
