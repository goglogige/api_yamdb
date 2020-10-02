from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return request.user.is_superuser and request.user.is_authenticated
        return True


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
