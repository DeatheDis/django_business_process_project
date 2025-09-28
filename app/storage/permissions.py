from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


class IsCompanyOwnerForStorage(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            return bool(
                user.is_authenticated
                and request.user.is_company_owner
                and request.user.company_id
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj.company and obj.company.owner_id == request.user.id:
            return True

        raise PermissionDenied('Вы не владелец этого склада')


class IsSameCompanyUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated and obj.company_id == request.user.company_id

        return True
