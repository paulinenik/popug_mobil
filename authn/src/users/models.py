import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models

from app.models import TextChoices


class User(AbstractUser):  # noqa
    objects: ClassVar[_UserManager] = _UserManager()

    class Roles(TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        DEVELOPER = "developer", "Developer"

    role = models.CharField(choices=Roles.choices, max_length=32)
    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    USERNAME_FIELD = "email"
