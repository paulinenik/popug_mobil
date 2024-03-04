from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    remote_addr = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "remote_addr",
            "role",
            "public_id",
        ]

    def get_remote_addr(self, obj: User) -> str:
        return self.context["request"].META["REMOTE_ADDR"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}
