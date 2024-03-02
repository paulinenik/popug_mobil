from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from users.api import viewsets

router = SimpleRouter()
router.register("", viewsets.UserViewSet, basename="users")

app_name = "users"
urlpatterns = [
    path("me/", viewsets.SelfView.as_view()),
    path("", include(router.urls)),
]
