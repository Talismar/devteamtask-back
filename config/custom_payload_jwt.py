from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore
from devteamtask.users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # token["email"] = user.email
        # token["groups"] = user.get_all_groups()
        # token["permissions"] = user.get_permissions

        return token
