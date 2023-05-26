from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    BooleanField,
    CASCADE,
    PROTECT,
    SET_NULL,
    SET_DEFAULT
)
from devteamtask.utils.projects import STATE
from devteamtask.projects.models import (
    Project,
    Tag,
    Status
)
from devteamtask.users.models import User


class Sprint(Model):
    name = CharField(max_length=120)
    description = TextField()
    state = CharField(max_length=2, choices=STATE.choices, default=STATE.IN_PROGRESS)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    project_id = ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
        return f"{self.pk} - {self.project_id.name}"

    class Meta:
        verbose_name = "Sprint"
        verbose_name_plural = "Sprints"


class Tasks(Model):
    name = CharField(max_length=120)
    description = TextField()
    tag = ForeignKey(Tag, on_delete=PROTECT, blank=True, null=True)
    status = ForeignKey(Status, on_delete=PROTECT)
    priority = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    assigned_to = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="task_assigned_to")
    created_by = ForeignKey(User, on_delete=SET_DEFAULT, default=1, related_name="task_created_by")
    project_id = ForeignKey(Project, on_delete=CASCADE)
    sprint_id = ForeignKey(Sprint, on_delete=PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.project_id.name}"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Notification(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=48)
    description = CharField(max_length=80)
    state = BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name}"
