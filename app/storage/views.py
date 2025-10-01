from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from storage.models import Storage
from .serializers import StorageSerializer
from rest_framework import mixins, viewsets
from .permissions import IsCompanyOwnerForStorage, IsSameCompanyUser

from drf_spectacular.utils import (
    extend_schema,
)


@extend_schema(
    tags=['Storage'],
    request=StorageSerializer,
)
class StorageViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsSameCompanyUser, IsCompanyOwnerForStorage]

    def get_queryset(self):
        user = self.request.user
        return Storage.objects.select_related('company', 'company__owner').filter(company_id=user.company_id)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
