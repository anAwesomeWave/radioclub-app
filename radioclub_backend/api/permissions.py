from rest_framework import permissions

from users.models import ADMIN_ROLES


class IsOwnerOrModerator(permissions.BasePermission):
    """Permission class. Checks that user is owner or has moder role."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
                (obj.author == request.user or request.user.is_admin or
                 request.user.is_moderator) and request.method == 'DELETE'
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Permission class. Check that only admin can get access."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and
                request.user.is_admin)


class Profile(permissions.BasePermission):
    """Permission class for getting access to the profile's page."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """ Определяет, может ли пользователь делать действия с объектом.
        смотреть могут все, админы могут менять role, а автор - все,
        кроме role
        """
        if (request.method in permissions.SAFE_METHODS or
                request.user.is_superuser):
            return True

        # если пользователь не автор и не админ
        if request.user != obj and not (request.user.is_moderator
                                        or request.user.is_admin):
            return False
        if request.user == obj:
            # пользователь - автор, провеяем, что он не указал role
            if request.user.is_admin:
                return True
            return 'role' not in request.data

        # админы могут только role менять
        if not (len(request.data) == 1 and 'role' in request.data):
            return False
        # if request.

        # адммины могу указывать любую роль а модераторы все кроме админских
        return (request.user.is_admin or
                request.user.is_moderator and request.data['role']
                not in ADMIN_ROLES)
