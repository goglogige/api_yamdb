from rest_framework.permissions import BasePermission


class IsAuthorOrIsStaffPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                request.method not in ('PATCH', 'DELETE')
                or (
                        request.user == obj.author
                        or request.user.is_staff
                )
        )
