from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object and admins to
    read/edit it else deny access.
    """

    def has_object_permission(self, request, view, obj):
        # Read/Write permissions are only allowed to the owner of the booking OR
        # to Admins
        return obj.owner == request.user or request.user.is_staff
