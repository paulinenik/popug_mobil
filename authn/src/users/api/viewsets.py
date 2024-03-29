from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django.db.models import QuerySet

from app.api.viewsets import CUDModelViewSet
from app.kafka.producer import Producer
from users.api.serializers import UserRegisterSerializer
from users.api.serializers import UserSerializer
from users.models import User


class SelfView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)


class UserViewSet(CUDModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    serializer_action_classes = {
        "create": UserRegisterSerializer,
        "update": UserSerializer,
        "partial_update": UserSerializer,
    }

    def get_permissions(self) -> list:
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self) -> "User":
        return self.get_queryset().get(pk=self.request.user.pk)

    def perform_create(self, serializer: Any) -> "User":  # type: ignore
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        Producer(event="UserCreated", topic="users-stream", data=UserSerializer(user).data)
        return user

    def perform_update(self, serializer: Any) -> "User":  # type: ignore
        user = super().perform_update(serializer)
        Producer(event="UserUpdated", topic="users-stream", data=serializer.data)
        return user

    def perform_destroy(self, instance: "User") -> None:
        public_id = instance.public_id
        super().perform_destroy(instance)
        Producer(event="UserDeleted", topic="users-stream", data={"public_id": public_id})
