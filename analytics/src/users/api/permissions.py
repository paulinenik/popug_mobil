from rest_framework import permissions


class ManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == request.user.Roles.MANAGER


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == request.user.Roles.ADMIN
