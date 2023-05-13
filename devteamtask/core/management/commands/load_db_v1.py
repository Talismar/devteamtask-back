from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


def create_default_group():
    groups_name = ["Administrator", "Master", "Owner", "Collaborator"]

    for group_name in groups_name:
        default = {"name": group_name}
        instance, created = Group.objects.get_or_create(name=group_name, defaults=default)
        print(created)


def create_default_user():
    print("Creating default user...")

    user_data = [
        {
            "username": "admin",
            "email": "admin.una@gmail.com",
            "password": 'argon2$argon2id$v=19$m=102400,t=2,p=8$WHQzS3ZaYWczQUYydTFZd2VmOU42VQ$CHpjmk76A/cU2C7W43ObB+tVkiUSNB86FRj3wDs9es4',  # noqa
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        },
        {
            "username": "deleted_user",
            "email": "deleted_user.una@gmail.com",
            "password": 'argon2$argon2id$v=19$m=102400,t=2,p=8$WHQzS3ZaYWczQUYydTFZd2VmOU42VQ$CHpjmk76A/cU2C7W43ObB+tVkiUSNB86FRj3wDs9es4',  # noqa
            "is_staff": True,
            "is_active": True,
        },
    ]

    for user in user_data:
        instance, created = User.objects.get_or_create(username=user["username"], defaults=user)
        print(created)


class Command(BaseCommand):
    help = "Load default data"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("CREATE GROUPS")
        )
        create_default_group()

        self.stdout.write(
            self.style.SUCCESS("CREATE USERS")
        )
        create_default_user()

        self.stdout.write(
            self.style.SUCCESS("DATA LOADING SUCCESS")
        )
