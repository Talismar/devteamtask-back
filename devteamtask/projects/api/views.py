from typing import Any, Type
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponseBase
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
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
from .serializers import (
    Project_CUD_Serializer,
    Project_LR_Serializer,
    InviteSerializer,
    TagSerializer,
    StatusSerializer,
    SprintSerializer,
    EventNoteSerializer,
    DailySerializer,
    EmailSerializer
)
from django.contrib.auth.models import Group
from devteamtask.utils.send_email_thred import SendEmailByThread
from django.db.models import Q
from django.shortcuts import redirect
from datetime import datetime
from django.utils.timezone import get_current_timezone, make_aware
from devteamtask.users.models import User
from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import serializers
from config.settings.base import env
from rest_framework.permissions import IsAuthenticated
from .permissions import UnauthenticatedGet


class ProjectViewSet(ModelViewSet):
    filterset_fields = ['leader', 'collaborators', 'product_owner']

    def __init__(self, *args, **kwargs):
        super(ProjectViewSet, self).__init__(*args, **kwargs)
        self._list_threads: list[SendEmailByThread] = []

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = Project.objects.filter(Q(leader=user.pk) | Q(collaborators__pk=user.pk) | Q(product_owner=user.pk))
        return queryset

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return Project_LR_Serializer

        return Project_CUD_Serializer

    def email_validation(self, request: Request):
        product_owner = request.data.pop("product_owner", False)
        collaborators = request.data.pop("collaborators", False)
        errors = {}
        has_error = False

        if product_owner:
            serializer_email = EmailSerializer(data={"email": product_owner})

            if serializer_email.is_valid():
                pass
            else:
                error_message = serializer_email.errors.pop("email")
                has_error = True
                errors["product_owner"] = error_message

        if collaborators:

            for enum, collaborator in enumerate(collaborators):
                serializer_email = EmailSerializer(data={"email": collaborator})

                if serializer_email.is_valid():
                    pass
                else:
                    error_message = serializer_email.errors.pop("email")
                    has_error = True
                    errors[f"collaborator {enum}"] = error_message

        return product_owner, collaborators, errors, has_error

    def send_email_collaborators(self, instance_project: Project | Any, emails: list[str]):
        for enum, email in enumerate(emails):
            thread_name = f"collaborator - {enum}"
            link = self.save_invite(instance_project, email, "Collaborator")

            send_email_thread = SendEmailByThread(thread_name, instance_project, email, link)
            self._list_threads.append(send_email_thread)
            send_email_thread.start()

    def save_invite(self, instance: Project | Any, email: str, group_name) -> str:
        data = {
            "project_id": instance,
            "email": email,
            "user_group": Group.objects.get(name=group_name)
        }

        new_invite = Invite.objects.create(**data)
        new_invite.save()

        return new_invite.token

    def send_emails(self, instance_project, product_owner: str, collaborators: list[str]):
        if product_owner:
            link = self.save_invite(instance_project, product_owner, 'Owner')
            send_email_thread = SendEmailByThread("product_owner", instance_project, product_owner, link)
            self._list_threads.append(send_email_thread)
            send_email_thread.start()

        if collaborators:
            self.send_email_collaborators(instance_project, collaborators)

    def add_email_send_status_in_serializer(self, serializer):
        # Await the threads to finish
        for thread in self._list_threads:
            serializer.data["email_send_status"] = True
            thread.join()

        # Check errors in email sending
        for thread in self._list_threads:
            has_error = thread.get_errors()
            if has_error:
                serializer.data["email_send_status"] = False
                break

        self._list_threads.clear()

    @extend_schema(request=inline_serializer(
        name="ProjectCreateSerializer",
        fields={
            "collaborators": serializers.ListField(child=serializers.EmailField()),
            "product_owner": serializers.EmailField(),
            "name": serializers.CharField(),
            "end_date": serializers.DateField()
        }
    ), responses=Project_LR_Serializer,
        description="If there are collaborators or product owner in the request body, the response will contain the email_send_state attribute included.")  # noqa: E501
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        product_owner, collaborators, errors, has_error = self.email_validation(request)

        if has_error:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if product_owner or collaborators:
            self.send_emails(serializer.instance, product_owner, collaborators)

        self.lookup_field = "pk"
        self.kwargs = {"pk": serializer.data["id"]}
        instance = self.get_object()
        serializer_response = Project_LR_Serializer(instance=instance)

        if product_owner or collaborators:
            self.add_email_send_status_in_serializer(serializer_response)

        return Response(serializer_response.data, status=status.HTTP_201_CREATED)


class TagViewSet(ListAPIView, RetrieveAPIView, CreateAPIView, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StatusViewSet(ListAPIView, RetrieveAPIView, CreateAPIView, GenericViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class InviteViewSet(RetrieveAPIView, CreateAPIView, GenericViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    lookup_field = 'token'
    permission_classes = [IsAuthenticated | UnauthenticatedGet]

    def __init__(self, *args, **kwargs):
        super(InviteViewSet, self).__init__(*args, **kwargs)
        self.redirect_front = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        response = super().dispatch(request, *args, **kwargs)

        if response.status_code == 404:
            messageError = "User or token not found. Please register your account before joining the project."
            response_redirect = redirect(f"{env('DDT_FRONT_URL')}/login")
            response_redirect.set_cookie("detail", messageError)
            return response_redirect

        return response

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance: Invite = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            user = User.objects.get(email=instance.email)
        except User.DoesNotExist:
            return Response({
                "detail": {
                    "User not found"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate token days
        today_date = datetime.now()
        today = make_aware(today_date, get_current_timezone())

        if not instance.expires > today:
            return Response({
                "error": {
                    "Token expired"
                }
            }, status=status.HTTP_404_NOT_FOUND)

        instance_project = Project.objects.get(pk=instance.project_id.pk)

        if instance.user_group.name == 'Owner':
            instance_project.product_owner = user
        else:
            # ManyToManyField
            instance_project.collaborators.add(user)

        instance_project.save()

        return Response(serializer.data)


class SprintViewSet(ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class EventNotesViewSet(RetrieveUpdateAPIView, ListAPIView, GenericViewSet):
    queryset = EventNotes.objects.all()
    serializer_class = EventNoteSerializer

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = EventNotes.objects.filter(Q(project__leader=user.pk))
        return queryset


class DailyViewSet(ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = DailySerializer
