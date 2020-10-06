from rest_framework.permissions import SAFE_METHODS, BasePermission


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


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrIsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS and
                request.user.is_anonymous or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return (obj.author == request.user or
                    request.user.is_staff or
                    request.user.is_superuser or
                    request.user.role in ['admin', 'moderator'])
        return True

