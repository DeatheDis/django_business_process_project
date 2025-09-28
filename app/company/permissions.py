from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            if obj.owner != request.user:
                raise PermissionDenied('Вы не владелец этой компании')
        return True
