from typing import Any
from devteamtask.users.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError
)
from collections import OrderedDict
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from config.settings.base import env
from django.conf import settings
from .google import Google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class GroupNestedSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    auth_provider = CharField(write_only=True, required=False)
    email = EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(),
        message="Email address already exists"
    )])
    name = CharField(required=True)
    groups = GroupNestedSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "password",
            "avatar_url",
            "phone_number",
            "groups",
            "is_staff",
            "is_active",
            "auth_provider"
        ]
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=['email'],
        #         message="Generic message for all errors"
        #     )
        # ]
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "email"},
        }

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        HTTP_ORIGIN = self.context["request"].META.get("HTTP_ORIGIN")
        is_frontend_request = HTTP_ORIGIN == env("DDT_FRONT_URL")

        if is_frontend_request:
            attrs["password"] = env("SOCIALACCOUNT_AUTH_PASSWORD")

            if not attrs.get("auth_provider", False):
                raise ValidationError("You must provide an auth provider.")

        elif len(attrs["password"]) > 8:
            raise ValidationError({
                "password": "Ensure this field has no more than 8 characters."
            })

        if not is_frontend_request and attrs.get("auth_provider", False):
            del attrs["auth_provider"]

        return attrs

    def create(self, validated_data) -> User:
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        has_password = validated_data.get('password', False)

        if has_password:
            validated_data["password"] = make_password(validated_data.get("password"))

        return super().update(instance, validated_data)


class ChangePasswordSerializer(Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class ChangePasswordByTokenSerializer(Serializer):
    model = User

    new_password = CharField(required=True)
    token = CharField(required=True)


class GoogleSocialAuthSerializer(Serializer):
    auth_token = CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:  # noqa: E722
            raise ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        print(user_data['aud'])
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        # user_id = user_data['sub']
        # email = user_data['email']
        # name = user_data['name']
        # provider = 'google'

        return {
            "user": user_data
        }

        # return register_social_user(
        #     provider=provider, user_id=user_id, email=email, name=name)
