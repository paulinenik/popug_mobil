from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class JSONWebTokenWithPublicIDAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """

        public_id = self.jwt_get_public_id_from_payload(payload)

        if not public_id:
            msg = _("Invalid payload.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            User = get_user_model()
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            msg = _("Invalid token.")
            raise exceptions.AuthenticationFailed(msg)

        return user

    def jwt_get_public_id_from_payload(self, payload):
        return payload.get("public_id")
