from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView
)
from devteamtask.projects.models import (
    Project,
    Tag,
    Status,
    Sprint,
    Invite
)
from .serializers import (
    ProjectSerializer,
    InviteSerializer,
    TagSerializer,
    StatusSerializer,
    SprintSerializer
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TagViewSet(ListAPIView, RetrieveAPIView, CreateAPIView, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StatusViewSet(ListAPIView, RetrieveAPIView, CreateAPIView, GenericViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class InviteViewSet(ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
