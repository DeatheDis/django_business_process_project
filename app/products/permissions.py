from rest_framework.permissions import BasePermission


class IsSameCompanyUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.company_id)

    def has_object_permission(self, request, view, obj):
        if not request.user.company_id:
            return False

        if hasattr(obj, 'storage'):
            obj_company_id = obj.storage.company_id
        elif hasattr(obj, 'company_id'):
            obj_company_id = obj.company_id
        elif hasattr(obj, 'supplier'):
            obj_company_id = obj.supplier.company_id
        else:
            return False

        return obj_company_id == request.user.company_id

