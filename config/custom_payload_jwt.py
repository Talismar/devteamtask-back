from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from devteamtask.users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["username"] = user.username
        # token["groups"] = user.get_all_groups()
        # token["permissions"] = user.get_permissions

        return token
