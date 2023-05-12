from typing import Any
from devteamtask.users.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class GroupNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    groups = GroupNestedSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
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

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

    def create(self, validated_data) -> User:
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance: User, validated_data: Any) -> User:
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
