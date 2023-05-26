from rest_framework.serializers import (
    ModelSerializer,
    BooleanField
)
from devteamtask.core.models import (
    Notification,
    Sprint,
    Tasks
)


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Tasks
        fields = "__all__"
        extra_kwargs = {
            'created_by': {'required': True}
        }


class SprintSerializer(ModelSerializer):

    class Meta:
        model = Sprint
        fields = "__all__"


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"
