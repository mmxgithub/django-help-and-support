from math import perm
from tokenize import Triple
from rest_framework import permissions

class StaffSelfAdminAll(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.assignee:
            return True
        if request.user.is_superuser:
            return True
        return False

class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser