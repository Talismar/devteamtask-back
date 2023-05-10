from typing import Any
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault
)
from devteamtask.projects.models import (
    Project,
    Tag,
    Status,
    Sprint,
    Invite
)


class ProjectSerializer(ModelSerializer):
    state = SerializerMethodField()
    # leader = HiddenField(write_only=True, default=CurrentUserDefault())

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {'leader': {'required': False}}

    # def validate(self, attrs):
    #     if attrs["amount"] > attrs["book"].amount:
    #         raise serializers.ValidationError({
    #             "leader": "Error"
    #         })
    #     return attrs

    def create(self, validated_data: Any) -> Any:
        validated_data['leader'] = self.context["request"].user
        return super().create(validated_data)

    def get_state(self, instance: Project) -> str:
        return instance.get_state_display()


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = "__all__"


class SprintSerializer(ModelSerializer):
    class Meta:
        model = Sprint
        fields = "__all__"
