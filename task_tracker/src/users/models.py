from typing import ClassVar
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django.db.models import TextChoices


class User(AbstractUser):  # noqa
    objects: ClassVar[_UserManager] = _UserManager()

    class Roles(TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        DEVELOPER = "developer", "Developer"

    role = models.CharField(choices=Roles.choices, max_length=32)
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)
