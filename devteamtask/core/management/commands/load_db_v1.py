from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


def create_default_group():
    groups_name = ["Administrator", "Master", "Onwer", "Collaborators"]

    for group_name in groups_name:
        default = {"name": group_name}
        instance, created = Group.objects.get_or_create(name=group_name, defaults=default)
        print(created)


def create_default_user():
    usernames = ["deleted", "admin"]


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        create_default_group()

        self.stdout.write(
            self.style.SUCCESS('Successfully closed poll "%s"' % "GROUPS")
        )
