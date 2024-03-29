# Generated by Django 4.1.9 on 2023-07-18 14:20

import devteamtask.utils.projects
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EventNotes",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("planning", models.TextField(blank=True, null=True)),
                ("review", models.TextField(blank=True, null=True)),
                ("retrospective", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Event notes",
                "verbose_name_plural": "Event notes",
                "db_table": "event_notes",
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=24)),
            ],
            options={
                "verbose_name": "Status",
                "verbose_name_plural": "Status",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=24)),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField()),
                (
                    "state",
                    models.CharField(choices=[("1", "IN_PROGRESS"), ("2", "FINISHED")], default="1", max_length=2),
                ),
                ("logo_url", models.ImageField(blank=True, null=True, upload_to="projects/logo")),
                (
                    "collaborators",
                    models.ManyToManyField(blank=True, related_name="collaborators", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "event_notes",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="projects.eventnotes"
                    ),
                ),
                (
                    "leader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="leader", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "product_owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("status", models.ManyToManyField(blank=True, related_name="status", to="projects.status")),
                ("tags", models.ManyToManyField(blank=True, related_name="tags", to="projects.tag")),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.CreateModel(
            name="Invite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254)),
                ("expires", models.DateTimeField(default=devteamtask.utils.projects.in_three_days)),
                ("token", models.CharField(default=devteamtask.utils.projects.get_url, max_length=24)),
                ("project_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="projects.project")),
                (
                    "user_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="user_group", to="auth.group"
                    ),
                ),
            ],
            options={
                "verbose_name": "Invite",
                "verbose_name_plural": "Invites",
            },
        ),
        migrations.CreateModel(
            name="Daily",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "event_notes_id",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="projects.eventnotes"),
                ),
            ],
            options={
                "verbose_name": "Daily",
                "verbose_name_plural": "Daily",
            },
        ),
    ]
