from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь админом или суперюзером.
    """
    def has_permission(self, request, view):
        is_safe = request.method in permissions.SAFE_METHODS
        if is_safe:
            return True
        return user_check(request.user)


class IsUserAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь автором поста или модератором.
    """
    def has_object_permission(self, request, view, obj):
        is_safe = request.method in permissions.SAFE_METHODS
        if is_safe:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.role == 'moderator':
            return True
        if obj.author == request.user:
            return True
        return False


class UsersMePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True


class IsAdminOrNoPermission(permissions.BasePermission):
    """
    Проверяет, является ли пользователь админом.
    """
    def has_permission(self, request, view):
        return user_check(request.user)


def user_check(user):
    if user.is_anonymous:
        return False
    is_superuser = user.is_superuser
    is_admin = user.role == 'admin'
    return is_superuser or is_admin
