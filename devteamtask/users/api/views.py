from typing import Any
from devteamtask.users.models import User
from rest_framework import status
from rest_framework.decorators import action
from devteamtask.utils.projects import in_three_days, get_url
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from devteamtask.projects.api.serializers import EmailSerializer
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import UnauthenticatedPost
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | UnauthenticatedPost]
    queryset = User.objects.all()
    # lookup_field = "email"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)

        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request: Request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        request=EmailSerializer,
        responses={200: None},
        methods=["POST"]
    )
    @action(detail=False, methods=['POST'])
    def reset_password(self, request: Request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance_user = get_object_or_404(User, email=serializer.data['email'])

        token = get_url()

        # Send email to instance
        instance_user.email_user("ola", "opa gente boa seu link de redificar sua senha: " + token)

        instance_user.token = token
        instance_user.expires = in_three_days()
        instance_user.save()

        return Response(status=status.HTTP_200_OK, data={"test": "password reset"})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None) -> User:
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateTokenPermanentlyByEmail(CreateAPIView):
    model = Token
    serializer_class = EmailSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, email=serializer.data["email"])

        token, created = self.model.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        }, status=status.HTTP_201_CREATED
        )


change_password_view = ChangePasswordView.as_view()
generate_token_permanently_by_email = GenerateTokenPermanentlyByEmail.as_view()
