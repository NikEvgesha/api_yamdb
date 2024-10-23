
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated and request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.is_superuser:
            return True
        if (request.method in SAFE_METHODS
                and request.user.is_authenticated):
            return True
        return False


class IsAuthorOrReadOnly(BasePermission):
    """
    Кастомное разрешение, которое позволяет редактировать объект только автору,
    а также модератору или администратору.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.is_superuser)
