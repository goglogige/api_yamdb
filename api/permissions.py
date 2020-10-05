from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdministrator(BasePermission):
    message = "You can't do this!"

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and (
                request.user.role == 'admin' or
                request.user.is_staff or
                request.user.is_superuser
            )
        )


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user.is_superuser and request.user.is_authenticated
        return True


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrIsStaffPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                request.method not in ('PATCH', 'DELETE')
                or (
                        request.user == obj.author
                        or request.user.is_staff
                )
        )

