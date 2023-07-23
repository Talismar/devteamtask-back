from typing import Any
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault,
    SlugRelatedField,
    ValidationError,
    EmailField,
    Serializer,
    IntegerField,
    UUIDField,
    PrimaryKeyRelatedField,
)
from devteamtask.projects.models import Project, Tag, Status, Invite, EventNotes, Daily
from collections import OrderedDict
from devteamtask.core.models import Sprint
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from devteamtask.projects.types import TagCreationDataType, StatusCreationDataType
from rest_flex_fields import FlexFieldsModelSerializer  # type: ignore
from devteamtask.core.api.serializers import RLTaskSerializer


User = get_user_model()


class CollaboratorsNestedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "avatar_url"]


class TagSerializer(ModelSerializer):
    project_id = UUIDField(write_only=True, required=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "project_id"]

    def create(self, validated_data: TagCreationDataType) -> Tag:
        name = validated_data.get("name")
        project_id = validated_data.pop("project_id")  # type: ignore

        # user = self.context["request"].user
        # project_ids = Project.objects.filter(Q(leader=user.pk) | Q(collaborators__pk=user.pk) |
        #  Q(product_owner=user.pk)).values_list("id", flat=True)

        # if not (project_id in project_ids):
        #     raise ValidationError({"error": "Sem permissão para criar tag"})

        default = {"name": name}
        instance_tag, created = Tag.objects.get_or_create(name__iexact=name, defaults=default)

        # Assign the instance to the project
        Project.objects.get(id=project_id).tags.add(instance_tag)

        return instance_tag


class StatusSerializer(ModelSerializer):
    project_id = UUIDField(write_only=True, required=True)

    class Meta:
        model = Status
        fields = ["id", "name", "project_id"]

    def create(self, validated_data: StatusCreationDataType) -> Status:
        name = validated_data.get("name")
        project_id = validated_data.pop("project_id")  # type: ignore

        default = {"name": name}
        instance_status, created = Status.objects.get_or_create(name__iexact=name, defaults=default)

        # Assign the instance to the project
        Project.objects.get(pk=project_id).status.add(instance_status)

        return instance_status


class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = "__all__"


class SprintSerializer(ModelSerializer):
    class Meta:
        model = Sprint
        fields = "__all__"


class Project_CUD_Serializer(ModelSerializer):
    leader = HiddenField(default=CurrentUserDefault())
    product_owner = EmailField(required=False)

    class Meta:
        model = Project
        fields = ["id", "leader", "end_date", "collaborators", "product_owner", "name", "logo_url"]
        extra_kwargs = {"leader": {"required": False}}

    def __init__(self, *args, **kwargs):
        super(Project_CUD_Serializer, self).__init__(*args, **kwargs)
        self._request: Request = self.context["request"]

    def has_attribute(self, attribute: str):
        return attribute in self._request.data

    def get_state(self, instance: Project) -> str:
        return instance.get_state_display()

    def create(self, validated_data: Any) -> Any:
        instance: Project = super().create(validated_data)
        instance.status.set([1, 2, 3])
        return instance


class Project_LR_Serializer(FlexFieldsModelSerializer):
    state = SerializerMethodField(read_only=True)
    status = StatusSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    collaborators = CollaboratorsNestedSerializer(read_only=True, many=True)
    product_owner: SlugRelatedField = SlugRelatedField(slug_field="email", read_only=True)
    leader = CollaboratorsNestedSerializer(read_only=True)
    tasks_set = RLTaskSerializer(many=True)
    sprint_set = SprintSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "state",
            "status",
            "tags",
            "collaborators",
            "product_owner",
            "leader",
            "name",
            "event_notes",
            "sprint_set",
            "tasks_set",
            "end_date",
            "logo_url",
        ]

    def get_state(self, instance: Project) -> str:
        return instance.get_state_display()


class EventNoteSerializer(ModelSerializer):
    daily_set = PrimaryKeyRelatedField(many=True, read_only=True)  # type: ignore

    class Meta:
        model = EventNotes
        fields = ["id", "planning", "review", "retrospective", "daily_set"]


class DailySerializer(ModelSerializer):
    class Meta:
        model = Daily
        fields = "__all__"


class EmailSerializer(Serializer):
    email = EmailField()
