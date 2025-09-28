from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import CompanySerializer
from .permissions import IsCompanyOwner
from company.models import Company

from drf_spectacular.utils import (
    extend_schema,
)


@extend_schema(
    tags=['Company'],
    request=CompanySerializer,
)
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.select_related('owner').all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        company = serializer.save(owner=self.request.user)
        user = self.request.user
        user.company = company
        user.is_company_owner = True
        user.save(update_fields=['company', 'is_company_owner'])

    def perform_destroy(self, instance):
        owner = instance.owner
        if owner.is_company_owner:
            owner.is_company_owner = False
            owner.save(update_fields=['is_company_owner'])

        instance.delete()

