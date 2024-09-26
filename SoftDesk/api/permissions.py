from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the resource.
        return obj.author == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to delete their own account only.
    """

    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are allowed to everyone.
        # if request.method in permissions.SAFE_METHODS:
            # return True
        # Only allow users to delete their own profile.
        return obj.pk == request.user.pk
