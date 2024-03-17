from users.models import User


def user_created_event_handler(data):
    public_id = data.pop("public_id")
    User.objects.update_or_create(
        public_id=public_id,
        defaults=data,
    )


def user_updated_event_handler(data):
    public_id = data.pop("public_id")
    User.objects.update_or_create(
        public_id=public_id,
        defaults=data,
    )


def user_deleted_event_handler(data):
    public_id = data.pop("public_id")
    User.objects.filter(public_id=public_id).delete()


users_stream_event_handlers = {
    "UserCreated": user_created_event_handler,
    "UserUpdated": user_updated_event_handler,
    "UserDeleted": user_deleted_event_handler,
}
