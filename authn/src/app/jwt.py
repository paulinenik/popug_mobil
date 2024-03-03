from typing import TYPE_CHECKING

from rest_framework_jwt.utils import jwt_create_payload

if TYPE_CHECKING:
    from users.models import User


def jwt_create_payload_with_public_id(user: "User"):
    payload = jwt_create_payload(user)
    payload["public_id"] = user.public_id
    return payload
