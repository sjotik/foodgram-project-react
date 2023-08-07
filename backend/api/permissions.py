from rest_framework import permissions


class IsAuthorOrAdmin(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_staff
                    or (request.user.is_authenticated
                        and obj.author == request.user))
        return request.method in permissions.SAFE_METHODS
