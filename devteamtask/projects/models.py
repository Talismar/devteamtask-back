from django.db.models import (
    Model,
    CharField,
    ManyToManyField,
    ForeignKey,
    DateField,
    DateTimeField,
    TextField,
    EmailField,
    ImageField,
    SET_NULL,
    CASCADE,
    PROTECT,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from devteamtask.utils.projects import in_three_days, get_url, STATE
from django.db.models.signals import post_save

User = get_user_model()


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


class EventNotes(Model):
    planning = TextField(blank=True, null=True)
    review = TextField(blank=True, null=True)
    retrospective = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Event notes"
        verbose_name_plural = "Event notes"
        db_table = "event_notes"


class Project(Model):
    name = CharField(max_length=120)
    start_date = DateField(auto_now_add=True)
    end_date = DateField()

    leader = ForeignKey(User, on_delete=CASCADE, related_name='leader')
    product_owner = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="product_owner")
    collaborators = ManyToManyField(User, related_name='collaborators', blank=True)

    tags = ManyToManyField(Tag, related_name="tags", blank=True)
    status = ManyToManyField(Status, related_name="status", blank=True)
    state = CharField(max_length=2, choices=STATE.choices, default=STATE.IN_PROGRESS)
    logo_url = ImageField(upload_to="projects/logo", blank=True, null=True)
    event_notes = ForeignKey(EventNotes, on_delete=PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Daily(Model):
    note = TextField()
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    event_notes_id = ForeignKey(EventNotes, on_delete=PROTECT)

    class Meta:
        verbose_name = "Daily"
        verbose_name_plural = "Daily"


"""
STUDIES:

PROTECT - O django irá lançar um error caso eu queira excluir um registro, ou seja
          irá proteger as tabelas que faz uso do registro.

SET_NULL - Atribuindo o atributt null=True se a instance for apagada ele vai atribuir
           null ao campo de relacionamento
"""


class Invite(Model):
    email = EmailField()
    project_id = ForeignKey(Project, on_delete=CASCADE)
    expires = DateTimeField(default=in_three_days)
    user_group = ForeignKey(Group, on_delete=PROTECT, related_name='user_group')
    token = CharField(max_length=24, default=get_url)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"
