from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault
)
from devteamtask.core.models import (
    Notification,
    Sprint,
    Tasks
)
from devteamtask.projects.models import (
    Status, Tag
)
from devteamtask.users.models import User


class StatusNestedSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TagNestedSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class UserNestedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "id", "avatar_url"]


class TaskSerializer(ModelSerializer):
    created_by = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Tasks
        fields = "__all__"
        # extra_kwargs = {
        #     'created_by': {'required': True}
        # }


class RLTaskSerializer(ModelSerializer):
    status = StatusNestedSerializer(read_only=True)
    tag = TagNestedSerializer(many=True)
    assigned_to = UserNestedSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = "__all__"


class SprintSerializer(ModelSerializer):

    class Meta:
        model = Sprint
        fields = "__all__"


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"
