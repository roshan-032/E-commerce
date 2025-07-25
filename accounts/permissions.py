from rest_framework.permissions import BasePermission

class IsAppAdmin(BasePermission):
    """
    Allows access only to app owner (admin).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_app_admin
