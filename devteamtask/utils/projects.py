from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.utils.timezone import get_current_timezone, make_aware
from django.db.models import TextChoices
from environ import Env


env = Env(
    DEBUG=(bool, False)
)

# reading .env file
Env.read_env()


def in_three_days():
    expires_date = datetime.now() + timedelta(days=3)
    naive_datetime = make_aware(expires_date, get_current_timezone())
    return naive_datetime


def get_url():
    return env("BACK_URL") + "token=" + get_random_string(length=24)


class STATE(TextChoices):
    IN_PROGRESS = "1", "IN_PROGRESS"
    FINISHED = "2", "FINISHED"
