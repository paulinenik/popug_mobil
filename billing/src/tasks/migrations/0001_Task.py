# Generated by Django 4.2.7 on 2024-03-17 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks.models.task


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("in_progress", "In Progress"), ("done", "Done")], default="in_progress", max_length=32)),
                ("public_id", models.UUIDField(unique=True)),
                ("fee", models.IntegerField(default=tasks.models.task.generate_task_fee)),
                ("reward", models.IntegerField(default=tasks.models.task.generate_task_reward)),
                ("assignee", models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
