from rest_framework.serializers import (
    ModelSerializer
)
from devteamtask.core.models import (
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
