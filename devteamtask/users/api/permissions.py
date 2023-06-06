from rest_framework.permissions import BasePermission


class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']


class UnauthenticatedPutOrPatch(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['PATCH', 'PUT']
