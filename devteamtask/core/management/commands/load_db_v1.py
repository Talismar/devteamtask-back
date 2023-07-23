from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from devteamtask.projects.models import Status


User = get_user_model()


def create_default_group():
    groups_name = ["Administrator", "Master", "Owner", "Collaborator"]

    for group_name in groups_name:
        default = {"name": group_name}
        Group.objects.get_or_create(name=group_name, defaults=default)


def create_default_status():
    default_status = ["To do", "Doing", "Done"]

    for enum, status_name in enumerate(default_status):
        default = {"name": status_name, "id": enum + 1}
        Status.objects.get_or_create(name=status_name, defaults=default)


def create_default_user():
    user_data = [
        {
            "email": "admin.una@gmail.com",
            "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$WHQzS3ZaYWczQUYydTFZd2VmOU42VQ$CHpjmk76A/cU2C7W43ObB+tVkiUSNB86FRj3wDs9es4",  # noqa
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        },
        {
            "email": "deleted_user.una@gmail.com",
            "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$WHQzS3ZaYWczQUYydTFZd2VmOU42VQ$CHpjmk76A/cU2C7W43ObB+tVkiUSNB86FRj3wDs9es4",  # noqa
            "is_staff": True,
            "is_active": True,
        },
    ]

    for user in user_data:
        User.objects.get_or_create(email=user["email"], defaults=user)


class Command(BaseCommand):
    help = "Load default data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Creating default groups"))
        create_default_group()

        self.stdout.write(self.style.SUCCESS("Creating default users"))
        create_default_user()

        self.stdout.write(self.style.SUCCESS("Creating default status"))
        create_default_status()

        self.stdout.write(self.style.SUCCESS("DATA LOADING SUCCESS"))
