from rest_framework.viewsets import (
    ModelViewSet
)
from devteamtask.core.models import (
    Sprint,
    Tasks
)
from .serializers import (
    TaskSerializer,
    SprintSerializer
)


class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
