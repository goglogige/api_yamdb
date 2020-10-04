from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    message = "You can't do this!"

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and (
                request.user.role == 'admin' or
                request.user.is_staff or
                request.user.is_superuser
            )
        )
