from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import ADMIN, MODERATOR


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class AuthorStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.role == ADMIN
                         or request.user.role == MODERATOR)))


class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        safe_actions = ('retrieve', 'partial_update',
                        'destroy', 'me',)
        if not request.user.is_authenticated:
            return False

        if not request.user.is_admin:
            if view.action == 'list':
                return False
            if request.method == 'POST':
                return False

        if view.action in safe_actions:
            return True

        return request.user.is_admin_access

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_owner = obj == user

        if request.method == 'PATCH' and view.action != 'me' and user.is_user:
            return False

        if request.method == 'DELETE' and view.action == 'me':
            return False

        if request.method == 'DELETE':
            return user.is_admin

        return user.is_admin or is_owner
