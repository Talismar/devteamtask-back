from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from devteamtask.users.api.views import (
    UserViewSet,
    # UserCreateViewSet,
    change_password_view
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
# router.register("users/create", UserCreateViewSet)


app_name = "api"
urlpatterns = [
    path("users/change-password/", change_password_view, name="change-password")
] + router.urls
