from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Any
from rest_framework.decorators import action
from rest_framework.request import Request

from app.api.viewsets import CreateRetrieveModelViewSet
from tasks.api.serializers.tasks import TaskCreateSerializer, TaskSerializer
from tasks.models import Task
from tasks.services.TaskCreator import TaskCreator
from tasks.services.TaskMarkCompleted import TaskMarkCompleted
from tasks.services.TaskReshuffle import TaskReshuffle
from users.api.permissions import AdminPermission, ManagerPermission


class TasksViewSet(CreateRetrieveModelViewSet):
    queryset = Task.objects.all()
    permissions = [IsAuthenticated]
    serializer_action_classes = {
        "create": TaskCreateSerializer,
        "retrieve": TaskSerializer,
        "list": TaskSerializer,
    }

    def get_queryset(self):
        if self.action in ["my", "mark_completed"]:
            return Task.objects.filter(assignee=self.request.user)
        return super().get_queryset()
    
    def perform_create(self, serializer: Any) -> "Task":
        return TaskCreator(data=serializer.validated_data)()

    @action(detail=True, methods=["post"])
    def mark_completed(self, request: "Request", *args: Any, **kwargs: Any) -> "Response":
        task = self.get_object()
        TaskMarkCompleted(instance=task)()
        return Response(200)

    @action(detail=False, methods=["get"])
    def my(self, request: "Request", *args: Any, **kwargs: Any) -> "Response":
        return self.list(request, *args, **kwargs)

    @action(detail=False, methods=["post"], permission_classes=[AdminPermission | ManagerPermission])
    def reshuflle(self, request: "Request", *args: Any, **kwargs: Any) -> "Response":
        TaskReshuffle()()
        return Response(200)
