from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from tasks.api.views.tasks import TasksViewSet

router = SimpleRouter()
router.register("", TasksViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
