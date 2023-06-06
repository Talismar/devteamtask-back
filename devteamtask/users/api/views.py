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
from .serializers import (UserSerializer, ChangePasswordSerializer, ChangePasswordByTokenSerializer,
                          GoogleSocialAuthSerializer)
from .permissions import UnauthenticatedPost, UnauthenticatedPutOrPatch
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils.timezone import get_current_timezone, make_aware
from config.settings.base import env
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | UnauthenticatedPost]
    queryset = User.objects.all()
    # lookup_field = "email"

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        print(request)
        return super().create(request, *args, **kwargs)

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
        auth_provider = instance_user.auth_provider

        if auth_provider is not None:
            error_message = "You cannot reset your password because your registration was made by " + auth_provider
            return Response(data={'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        token = get_url()
        subject = "Reset password"
        link = f"<a href='{env('DDT_FRONT_URL') + '/reset-password/?' + token}'>Link</a>"
        message = "Link to reset your password: " + link

        # Send email to instance
        instance_user.email_user(subject, "", "DevTeamTask", html_message=message)

        instance_user.token = token
        instance_user.expires = in_three_days()
        instance_user.save()

        return Response(status=status.HTTP_200_OK, data={"detail": "Link sent successfully"})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password - Authenticated
    """

    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None) -> User:
        obj = self.request.user
        return obj  # type: ignore

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


class ChangePasswordByToken(UpdateAPIView):
    """
    An endpoint for changing password - Unauthenticated - By Token
    """

    model = User
    permission_classes = [UnauthenticatedPutOrPatch]
    serializer_class = ChangePasswordByTokenSerializer

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        partial = kwargs.pop('partial', False)
        token = request.data.get('token', False)

        if not token:
            return Response(data={'token': "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance: User = User.objects.get(token=token)
            serializer = self.get_serializer(data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Validate token days
            today_date = datetime.now()
            today = make_aware(today_date, get_current_timezone())

            if isinstance(instance.expires, datetime):
                if not instance.expires > today:
                    return Response(data={'token': "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)

            instance.set_password(serializer.data.get('new_password'))
            # instance.token = None
            instance.save()

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            errors = {
                "detail": "Invalid token"
            }
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class GeneratePermanentTokenByProvider(CreateAPIView):
    model = Token
    serializer_class = EmailSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token, created = self.model.objects.get_or_create(user=request.user)

        return Response({
            "token": token.key
        }, status=status.HTTP_201_CREATED
        )


@permission_classes((AllowAny, ))
class GoogleSocialAuthView(GenericAPIView):  # type: ignore

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


change_password_view = ChangePasswordView.as_view()
change_password_by_token_view = ChangePasswordByToken.as_view()
generate_permanent_token_by_provider = GeneratePermanentTokenByProvider.as_view()
