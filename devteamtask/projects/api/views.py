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
from threading import Thread
from time import sleep
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.serializers import EmailField, Serializer
from django.contrib.auth.models import Group


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    filterset_fields = ['leader', 'collaborators', 'product_onwer']

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
                return Response({"product_onwer": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if collaborators:
            errors_emails = []
            has_errors = False
            for enum, collaborator in enumerate(collaborators):
                serializer_email = EmailSerializer(data={"email": product_onwer})

                if serializer_email.is_valid():
                    pass
                else:
                    has_errors = True
                    error_message = serializer_email.errors.pop("email")
                    errors_emails.append({
                        f"collaborator {enum}": error_message
                    })

            if has_errors:
                return Response({"collaborators": errors_emails}, status=status.HTTP_400_BAD_REQUEST)

        return product_onwer, collaborators

    def save_invite_and_send_email(self, instance: Project, email: str):
        print("Email sending")

        data = {
            "project_id": instance,
            "email": email,
            "user_group": Group.objects.get(id=1)
        }

        new_invite = Invite.objects.create(**data)
        new_invite.save()

        send_mail(
            subject="Title",
            message="Link" + str(new_invite.link),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["talismar788.una@gmail.com"]
        )

        # t1 = Thread(target=send_mail, args=(1.2,), name="SEND_EMAIL_OWNER")
        # t1.start()

    def send_email_collaborators(self, instance: Project, emails: list[str]):
        for email in emails:
            self.send_email_collaborators(instance, email)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        product_onwer, collaborators = self.email_validation(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer_response = {
            "data": {
                **serializer.data,
                "leader": request.user.email
            }
        }

        if product_onwer:
            self.save_invite_and_send_email(serializer.instance, product_onwer)

        if collaborators:
            self.send_email_collaborators(serializer.instance, collaborators)

        # self.lookup_field = "pk"
        # self.kwargs = {"pk": serializer.data["id"]}
        # instance = self.get_object()
        # serializer_response = Project_LR_Serializer(instance=instance)

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
