from rest_framework import permissions

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and (request.user.is_superuser or request.user.staff.is_admin)