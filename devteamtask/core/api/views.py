from typing import Any
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)
from devteamtask.core.models import (
    Notification,
    Sprint,
    Tasks
)
from .serializers import (
    NotificationSerializer,
    TaskSerializer,
    SprintSerializer
)
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST


class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class NotificationViewSet(ListAPIView, DestroyAPIView, UpdateAPIView, GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet:

        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()

        user = self.request.user
        queryset = Notification.objects.filter(user=user, state=True)  # type: ignore

        return Notification.objects.all()

    @extend_schema(request=inline_serializer(
        name="NotificationInlineSerializer",
        fields={
            "state": serializers.CharField()
        }),
        responses=NotificationSerializer
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        state = request.data.get('state', False)

        has_errors = False
        data = {}
        if not state:
            has_errors = True
            data["state"] = "This field is required."

        if len(request.data) > 1:
            has_errors = True
            data["error"] = "There is an unsupported field."

        if has_errors:
            return Response(data, status=HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)
