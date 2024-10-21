
from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated and request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.is_superuser:
            return True
        if (request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated):
            return True
        return False
