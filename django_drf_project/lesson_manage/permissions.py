from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        elif view.action == "update" or view.action == "partial_update":  # Обработка обновления только одного поля
            return request.user.groups.filter(name='Moderators').exists()
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif view.action == "update" or view.action == "partial_update":
            return request.user.groups.filter(name='Moderators').exists()
        return request.user == obj.owner