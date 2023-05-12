from typing import Any
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault,
    SlugRelatedField,
    ValidationError,
    EmailField,
    Serializer
)
from devteamtask.projects.models import (
    Project,
    Tag,
    Status,
    Invite,
    EventNotes,
    Daily
)
from devteamtask.core.models import Sprint
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.response import Response
# from devteamtask.core.api.serializers import SprintSerializer


User = get_user_model()


class CollaboratorsNestedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data: Any) -> Any:
        project_id = self.context["request"].data.get("project_id", False)
        instance = super().create(validated_data)

        Project.objects.get(pk=project_id).tags.add(instance)

        return instance


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

    def create(self, validated_data: Any) -> Any:
        project_id = self.context["request"].data.get("project_id", False)
        instance = super().create(validated_data)

        Project.objects.get(pk=project_id).status.add(instance)

        return instance


class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = "__all__"


class SprintSerializer(ModelSerializer):
    class Meta:
        model = Sprint
        fields = "__all__"


class Project_CUD_Serializer(ModelSerializer):
    state = SerializerMethodField(read_only=True)
    leader = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            'leader': {'required': False}
        }

    def __init__(self, *args, **kwargs):
        super(Project_CUD_Serializer, self).__init__(*args, **kwargs)
        self._request: Request = self.context["request"]

    def has_attribute(self, attribute: str):
        return attribute in self._request.data

    def get_state(self, instance: Project) -> str:
        return instance.get_state_display()

    def get_status_ids_default(self):
        status_default = ["To do", "Doing", "Done"]
        status_ids = []
        for status_name in status_default:
            default = {"name": status_name}
            instance, created = Status.objects.get_or_create(name=status_name, defaults=default)
            status_ids.append(instance.id)

        return status_ids

    def create(self, validated_data: Any) -> Any:
        instance: Project = super().create(validated_data)
        instance.status.set(self.get_status_ids_default())
        return instance


class Project_LR_Serializer(ModelSerializer):
    state = SerializerMethodField(read_only=True)
    status = StatusSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    collaborators = CollaboratorsNestedSerializer(read_only=True, many=True)
    product_onwer: SlugRelatedField = SlugRelatedField(slug_field='email', read_only=True)
    leader = CollaboratorsNestedSerializer(read_only=True)
    # sprint_set = SprintSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "state",
            "status",
            "tags",
            "collaborators",
            "product_onwer",
            "leader",
            # "sprint_set"
        ]

    def get_state(self, instance: Project) -> str:
        return instance.get_state_display()


class EventNoteSerializer(ModelSerializer):
    class Meta:
        model = EventNotes
        fields = "__all__"


class DailySerializer(ModelSerializer):
    class Meta:
        model = Daily
        fields = "__all__"


class EmailSerializer(Serializer):
    email = EmailField()
