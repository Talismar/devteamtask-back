from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from devteamtask.users.api.views import (
    UserViewSet,
    change_password_view
)
from devteamtask.projects.api.views import (
    ProjectViewSet,
    TagViewSet,
    StatusViewSet,
    InviteViewSet,
    SprintViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
# else:
#     router = SimpleRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("tags", TagViewSet)
router.register("status", StatusViewSet)
router.register("invite", InviteViewSet)
router.register("sprints", SprintViewSet)


app_name = "api"
urlpatterns = [
    path("users/change-password/", change_password_view, name="change-password")
] + router.urls
