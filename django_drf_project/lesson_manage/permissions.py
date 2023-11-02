
from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            return True
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated and (request.user.is_staff or
                   request.user.groups.filter(name='Moderators').exists())
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and (request.user.is_staff or
                   request.user.groups.filter(name='Moderators').exists() or
                   obj.owner == request.user)
        return False