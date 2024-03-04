# Generated by Django 4.2.7 on 2024-03-02 20:16

import uuid

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="public_id",
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(choices=[("admin", "Admin"), ("manager", "Manager"), ("developer", "Developer")], default="developer", max_length=32),
            preserve_default=False,
        ),
    ]
