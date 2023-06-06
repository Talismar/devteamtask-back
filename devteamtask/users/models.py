from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    ImageField,
    DateTimeField,
    BooleanField,
    EmailField
)
from django.urls import reverse
from devteamtask.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for DevTeamTask.
    """

    name = CharField(blank=True, max_length=255)
    avatar_url = ImageField(upload_to="users/photos", blank=True, null=True)
    phone_number = CharField(blank=True, max_length=32)
    token = CharField(max_length=24, null=True, blank=True)
    expires = DateTimeField(blank=True, null=True)
    notification_state = BooleanField(default=True)
    email = EmailField(unique=True)
    auth_provider = CharField(blank=True, null=True, max_length=10)

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore

    def __str__(self):
        return self.email

    def getAllGroups(self):
        return self.groups.all().values()
