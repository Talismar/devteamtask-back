from rest_framework.permissions import BasePermission


class UnauthenticatedGet(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']
