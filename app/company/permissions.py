from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            if obj.owner != request.user:
                raise PermissionDenied('Вы не владелец этой компании')
        return True


class CanCreateCompany(BasePermission):
    def has_permission(self, request, view):
        if getattr(view, 'action', None) == 'create':
            user = request.user
            return bool(user.is_authenticated and user.company_id is None)
        return True
