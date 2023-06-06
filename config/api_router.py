from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from devteamtask.users.api.views import (
    UserViewSet,
    GoogleSocialAuthView,
    change_password_view,
    change_password_by_token_view,
    generate_permanent_token_by_provider,
)
from devteamtask.projects.api.views import (
    ProjectViewSet,
    TagViewSet,
    StatusViewSet,
    InviteViewSet,
    EventNotesViewSet,
    DailyViewSet
)
from devteamtask.core.api.views import (
    TaskViewSet,
    SprintViewSet,
    NotificationViewSet
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()  # type: ignore

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet, basename="projects")
router.register("tags", TagViewSet)
router.register("status", StatusViewSet)
router.register("invite", InviteViewSet)
router.register("sprints", SprintViewSet)
router.register("tasks", TaskViewSet)
router.register("event-note", EventNotesViewSet)
router.register("daily", DailyViewSet)
router.register("notifications", NotificationViewSet, basename="notifications")


app_name = "api"
urlpatterns = [
    path("users/change-password/", change_password_view),
    path("users/change-password-by-token/", change_password_by_token_view),
    path("auth/token/permanent/provider/", generate_permanent_token_by_provider),
    path('auth/google/', GoogleSocialAuthView.as_view()),
] + router.urls
