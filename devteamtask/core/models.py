from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    IntegerField,
    ManyToManyField,
    ForeignKey,
    BooleanField,
    CASCADE,
    PROTECT,
    SET_NULL,
    SET_DEFAULT,
    Q,
)
from devteamtask.utils.projects import STATE
from devteamtask.projects.models import Project, Tag, Status
from devteamtask.users.models import User
from datetime import datetime, timedelta


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
    description = TextField(blank=True, null=True)
    tag = ManyToManyField(Tag, blank=True)
    status = ForeignKey(Status, on_delete=PROTECT)
    priority = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    assigned_to = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name="task_assigned_to")
    created_by = ForeignKey(User, on_delete=SET_DEFAULT, default=1, related_name="task_created_by")
    project_id = ForeignKey(Project, on_delete=CASCADE)
    sprint_id = ForeignKey(Sprint, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.project_id.name}"

    @classmethod
    def get_total_completed(cls, user: User):
        status_instance, created = Status.objects.get_or_create(name="Done")
        return cls.objects.filter(status=status_instance, assigned_to=user).count()

    @classmethod
    def get_total_assigned(cls, user: User):
        return cls.objects.filter(assigned_to=user).count()

    @classmethod
    def get_total_completed_in_last_7_days(cls, user: User):
        status_instance, created = Status.objects.get_or_create(name="Done")
        queryset = cls.objects.filter(
            assigned_to=user, status=status_instance, updated_at__gte=datetime.now() - timedelta(days=7)
        )

        def total_by_date(date: datetime):
            return cls.objects.filter(
                assigned_to=user, status=status_instance, updated_at__contains=str(date.date())
            ).count()

        data = []
        for item in queryset:
            data.append({"date": item.updated_at.date(), "amount": total_by_date(item.updated_at)})

        return data

    @classmethod
    def get_total_pending_in_last_7_days(cls, user: User):
        status_instance, created = Status.objects.get_or_create(name="To do")

        return cls.objects.filter(
            assigned_to=user, status=status_instance, updated_at__gte=datetime.now() - timedelta(days=7)
        ).count()

    @staticmethod
    def get_total_task_in_last_7_days(user: User):
        return Tasks.objects.filter(
            Q(project_id__leader=user.pk)
            | Q(project_id__collaborators__pk=user.pk)
            | Q(project_id__product_owner=user.pk),
            assigned_to__isnull=True,
            updated_at__gte=datetime.now() - timedelta(days=7),
        ).count()

    @staticmethod
    def get_total_scheduled(user: User):
        return Tasks.objects.filter(
            Q(project_id__leader=user.pk)
            | Q(project_id__collaborators__pk=user.pk)
            | Q(project_id__product_owner=user.pk),
            assigned_to__isnull=True,
        ).count()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Notification(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=120)
    description = CharField(max_length=80)
    state = BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name}"
