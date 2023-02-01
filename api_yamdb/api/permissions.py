from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Проверяет, является ли пользователь админом или суперюзером.
    """
    def has_permission(self, request, view):
        is_safe = request.method in permissions.SAFE_METHODS
        if is_safe:
            return True
        if not request.user.is_authentificated:
            return False
        is_superuser = request.user.is_superuser
        is_admin = request.user.role == "admin"
        return is_superuser or is_admin
