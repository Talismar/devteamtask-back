from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from devteamtask.projects.models import Project
from rest_framework.permissions import IsAuthenticated


class UnauthenticatedGet(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return request.method in ['GET']


class IsProjectLeader(BasePermission):
    message = "Project leader"

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user

        instance = get_object_or_404(Project, pk=view.kwargs.get("pk", None))

        if instance.leader == user:
            return True

        return IsAuthenticated.has_permission(self, request, view)
