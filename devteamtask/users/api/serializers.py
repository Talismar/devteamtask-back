from typing import Any
from devteamtask.users.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from config.settings.base import env


class GroupNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(),
        message="Email address already exists"
    )])
    name = serializers.CharField(required=True)
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
            "is_superuser",
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

    def validate(self, attrs: Any) -> Any:

        if self.context["request"].META.get("HTTP_ORIGIN") == env("DDT_FRONT_URL"):
            attrs["password"] = env("SOCIALACCOUNT_AUTH_PASSWORD")

        elif len(attrs["password"]) > 8:
            raise serializers.ValidationError({
                "password": "Ensure this field has no more than 8 characters."
            })

        return attrs

    def create(self, validated_data) -> User:
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        has_password = validated_data.get('password', False)

        if has_password:
            validated_data["password"] = make_password(validated_data.get("password"))

        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
