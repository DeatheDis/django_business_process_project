from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.owner_id != request.user.id:
            raise PermissionDenied('Вы не владелец этой компании')
        return True


class CanCreateCompany(BasePermission):
    def has_permission(self, request, view):
        if getattr(view, 'action', None) == 'create':
            user = request.user
            if not user.is_authenticated:
                return False
            if user.company_id is not None:
                raise PermissionDenied('Вы уже состоите в компании и не можете создать новую')
        return True
