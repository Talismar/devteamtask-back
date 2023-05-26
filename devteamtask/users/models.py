from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    ImageField,
    DateTimeField,
    BooleanField,
    EmailField
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from devteamtask.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for DevTeamTask.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    avatar_url = ImageField(upload_to="users/photos", blank=True, null=True)
    phone_number = CharField(_("Phone Number"), blank=True, max_length=32)
    token = CharField(max_length=24, null=True, blank=True)
    expires = DateTimeField(blank=True, null=True)
    notification_state = BooleanField(default=True)
    email = EmailField(_("email address"), unique=True)

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"email": self.email})
