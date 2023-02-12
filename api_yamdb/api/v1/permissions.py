from rest_framework import permissions
from reviews.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь админом или суперюзером.
    """
    def has_permission(self, request, view):
        is_safe = request.method in permissions.SAFE_METHODS
        return (
            is_safe
            or check_user_is_admin_or_superuser(request.user)
        )


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
        if request.user.role == User.MODERATOR:
            return True
        if obj.author == request.user:
            return True
        return False


class UsersEndpointPermission(permissions.BasePermission):
    """
    Проверяет, является ли пользователь админом.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if view.action in ('destroy', 'create', 'list'):
            return request.user.is_admin
        return True

    def has_object_permission(self, request, view, obj):
        if view.kwargs.get('username') == 'me':
            return True
        return check_user_is_admin_or_superuser(request.user)


class AuthorOrModeratorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role == User.ADMIN
                    or request.user.role == User.MODERATOR
                )
            )
        )


class AuthorAndStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin
                )
            )
        )


def check_user_is_admin_or_superuser(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.is_admin
        )
    )


class OwnerOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
