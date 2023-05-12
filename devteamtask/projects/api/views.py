from typing import Any, Type
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
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
from rest_framework.serializers import EmailField, Serializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    filterset_fields = ['leader', 'collaborators', 'product_onwer']

    def __init__(self, *args, **kwargs):
        super(ProjectViewSet, self).__init__(*args, **kwargs)
        self._list_threads: list[SendEmailByThread] = []

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in ["list", "retrieve"]:
            return Project_LR_Serializer

        return Project_CUD_Serializer

    def email_validation(self, request: Request):
        product_onwer = request.data.pop("product_onwer", False)
        collaborators = request.data.pop("collaborators", False)

        if product_onwer:
            serializer_email = EmailSerializer(data={"email": product_onwer})

            if serializer_email.is_valid():
                pass
            else:
                error_message = serializer_email.errors.pop("email")
                return {"product_onwer": error_message}, False

        if collaborators:
            errors_emails = []
            has_errors = False
            for enum, collaborator in enumerate(collaborators):
                serializer_email = EmailSerializer(data={"email": collaborator})

                if serializer_email.is_valid():
                    pass
                else:
                    has_errors = True
                    error_message = serializer_email.errors.pop("email")
                    errors_emails.append({
                        f"collaborator {enum}": error_message
                    })

            if has_errors:
                return product_onwer, {"collaborators": errors_emails}

        return product_onwer, collaborators

    def send_email_collaborators(self, instance: Project, emails: list[str]):
        for enum, email in enumerate(emails):
            thread_name = f"collaborator - {enum}"
            link = self.save_invite(instance, email)

            send_email_thread = SendEmailByThread(thread_name, instance, email, link)
            self._list_threads.append(send_email_thread)
            send_email_thread.start()

    def save_invite(self, instance: Project, email: str) -> str:
        data = {
            "project_id": instance,
            "email": email,
            "user_group": Group.objects.get(id=1)
        }

        new_invite = Invite.objects.create(**data)
        new_invite.save()

        return new_invite.link

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        product_onwer, collaborators = self.email_validation(request)

        if type(collaborators) == dict:
            return Response(collaborators, status=status.HTTP_400_BAD_REQUEST)

        if type(product_onwer) == dict:
            return Response(product_onwer, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if product_onwer:
            link = self.save_invite(serializer.instance, product_onwer)
            send_email_thread = SendEmailByThread("product_onwer", serializer.instance, product_onwer, link)
            self._list_threads.append(send_email_thread)
            send_email_thread.start()

        if collaborators:
            self.send_email_collaborators(serializer.instance, collaborators)

        # self.lookup_field = "pk"
        # self.kwargs = {"pk": serializer.data["id"]}
        # instance = self.get_object()
        # serializer_response = Project_LR_Serializer(instance=instance

        # Await the threads to finish
        for thread in self._list_threads:
            print(thread.thread_name)
            thread.join()

        errors_in_sending = False
        for thread in self._list_threads:
            errors_in_sending = thread.get_errors()
            if errors_in_sending:
                break

        serializer_response = {
            "data": {
                **serializer.data,
                "leader": request.user.email,
            }
        }

        return Response(serializer_response["data"], status=status.HTTP_201_CREATED, headers=headers)


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


class EventNotesViewSet(ModelViewSet):
    queryset = EventNotes.objects.all()
    serializer_class = EventNoteSerializer


class DailyViewSet(ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = DailySerializer
