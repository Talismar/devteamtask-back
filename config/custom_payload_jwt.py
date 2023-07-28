from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore
from devteamtask.users.models import User
from devteamtask.utils.logger import Logger


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        logger = Logger()

        if hasattr(logger, "info"):
            logger.info(f"User authenticated - {user.email}")

        return token
