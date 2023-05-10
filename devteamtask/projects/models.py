from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    ForeignKey,
    DateField,
    DateTimeField,
    TextField,
    EmailField,
    TextChoices,
    SET_NULL,
    CASCADE,
    PROTECT
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from devteamtask.utils.projects import in_three_days, get_url


User = get_user_model()


class Sprint(Model):

    class STATE(TextChoices):
        IN_PROGRESS = "1", "IN_PROGRESS"
        FINISHED = "2", "FINISHED"

    name = CharField(max_length=120)
    description = TextField()
    state = CharField(max_length=2, choices=STATE.choices, default=STATE.IN_PROGRESS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sprint"
        verbose_name_plural = "Sprints"


class Tag(Model):
    name = CharField(max_length=24)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Status(Model):
    name = CharField(max_length=24)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"


class Project(Model):

    class STATE(TextChoices):
        IN_PROGRESS = "1", "IN_PROGRESS"
        FINISHED = "2", "FINISHED"

    name = CharField(max_length=120)
    start_data = DateField(auto_now_add=True)
    end_data = DateField()
    leader = ForeignKey(User, on_delete=CASCADE, related_name='leader')
    product_onwer = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="product_onwer")
    collaborators = ManyToManyField(User, related_name='collaborators', blank=True)
    sprints = ManyToManyField(Sprint, related_name="sprints", blank=True)
    tags = ManyToManyField(Tag, related_name="tags", blank=True)
    status = ManyToManyField(Status, related_name="status", blank=True)
    state = CharField(max_length=2, choices=STATE.choices, default=STATE.IN_PROGRESS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


"""
STUDIES:

PROTECT - O django irá lançar um error caso eu queira excluir um grupo, ou seja
          irá proteger as tabelas que faz uso da entity.
"""


class Invite(Model):
    email = EmailField()
    project_id = ForeignKey(Project, on_delete=CASCADE)
    expires = DateTimeField(default=in_three_days)
    user_group = ForeignKey(Group, on_delete=PROTECT, related_name='user_group')
    link = CharField(max_length=24, default=get_url)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"
