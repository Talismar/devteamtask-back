from typing import Any
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from config.settings.base import env, MEDIA_URL
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from devteamtask.core.models import Notification, Sprint, Tasks, Status
from .serializers import NotificationSerializer, TaskSerializer, SprintSerializer, RLTaskSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from devteamtask.users.models import User


class TaskViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        status_instance = Status.objects.get(id=serializer.data["status"])
        user_instance: User | None = None

        if type(serializer.data["assigned_to"]) == int:
            user_instance = User.objects.get(id=serializer.data["assigned_to"])
            data = {
                **serializer.data,
                "status": {"id": status_instance.id, "name": status_instance.name},
            }

        data = {**serializer.data, "status": {"id": status_instance.id, "name": status_instance.name}}

        if user_instance is not None:
            data.update(
                {"assigned_to": {"id": user_instance.id, "name": user_instance.name, "email": user_instance.email}}
            )

            try:
                if isinstance(user_instance.avatar_url.url, str):
                    data["assigned_to"].update(
                        {"avatar_url": f"{env('BACK_URL')}{MEDIA_URL}{user_instance.avatar_url}"}
                    )
            except ValueError:
                pass

        return Response(data, status=HTTP_200_OK)

    @action(detail=False)
    def dashboard_data(self, request: Request) -> Response:
        data = {
            "total_completed": Tasks.get_total_completed(request.user),  # type: ignore
            "total_assigned": Tasks.get_total_assigned(request.user),  # type: ignore
            "total_scheduled": Tasks.get_total_scheduled(request.user),  # type: ignore
            "total_completed_by_day_in_last_7_days": Tasks.get_total_completed_in_last_7_days(request.user),  # type: ignore  # noqa: E501
            "total_pending_in_last_7_days": Tasks.get_total_pending_in_last_7_days(request.user),  # type: ignore
            "total_task_in_last_7_days": Tasks.get_total_task_in_last_7_days(request.user),  # type: ignore
        }
        return Response(data, status=HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        self.lookup_field = "pk"
        self.kwargs = {"pk": serializer.data["id"]}
        instance = self.get_object()
        serializer_response = RLTaskSerializer(instance=instance, context={"request": request})

        return Response(serializer_response.data, status=HTTP_201_CREATED)


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class NotificationViewSet(ListAPIView, DestroyAPIView, UpdateAPIView, GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self) -> QuerySet:
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()

        user = self.request.user
        if user.notification_state is True:  # type: ignore
            queryset = Notification.objects.filter(user=user, state=True)  # type: ignore

            return queryset

        return []  # type: ignore

    @extend_schema(
        request=inline_serializer(name="NotificationInlineSerializer", fields={"state": serializers.CharField()}),
        responses=NotificationSerializer,
    )
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        state = request.data.get("state", None)

        has_errors = False
        data = {}
        if state is None:
            has_errors = True
            data["state"] = "This field is required."

        if len(request.data) > 1:
            has_errors = True
            data["error"] = "There is an unsupported field."

        if has_errors:
            return Response(data, status=HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)
