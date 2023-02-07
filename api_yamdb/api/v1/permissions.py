from rest_framework import permissions


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
        if request.user.role == "moderator":
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
        if request.user.is_anonymous:
            return False
        if request.user.role == "admin":
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
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator'
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
