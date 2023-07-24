from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, SerializerMethodField
from devteamtask.core.models import Notification, Sprint, Tasks
from devteamtask.projects.models import Status, Tag
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
    avatar_url = SerializerMethodField()

    class Meta:
        model = User
        fields = ["name", "email", "id", "avatar_url"]

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        try:
            if obj.avatar_url and hasattr(obj.avatar_url, "url"):
                return request.build_absolute_uri(obj.avatar_url.url)  # type: ignore
        except ValueError:
            pass
        return None


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
