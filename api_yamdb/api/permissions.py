
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin or request.user.is_superuser:
            return True
        return False


class IsAdminOrSuperuserOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if (request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)):
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
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser)
