from typing import Any
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
from rest_framework.generics import CreateAPIView
from devteamtask.users.models import User
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer
)
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth.hashers import check_password


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AuthProviderSerializer(Serializer):
    password = CharField(required=True)
    auth_provider = CharField(required=True)
    email = EmailField(required=True)


class AuthProviderViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthProviderSerializer
    permission_classes = []

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        auth_provider = serializer.data["auth_provider"]
        password = serializer.data["password"]
        error_data = {"detail": "No active account found with the given credentials"}

        try:
            user: User = User.objects.get(email=email, auth_provider=auth_provider)
        except User.DoesNotExist:
            return Response(error_data, status=HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response(error_data, status=HTTP_401_UNAUTHORIZED)

        token = get_tokens_for_user(user)

        return Response(token, status=HTTP_200_OK)
