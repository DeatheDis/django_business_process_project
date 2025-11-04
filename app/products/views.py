from products.models import Supplier, Supply, Product
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from products.serializers import SupplierSerializer, SupplySerializer, ProductSerializer
from .permissions import IsSameCompanyUser
from drf_spectacular.utils import (
    extend_schema,
)


@extend_schema(
    tags=['Supplier'],
    request=SupplierSerializer,
)
class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSameCompanyUser]

    def get_queryset(self):
        user = self.request.user
        return Supplier.objects.select_related('company').filter(company_id=user.company_id).order_by('title')


@extend_schema(
    tags=['Supply'],
    request=SupplySerializer,
)
class SupplyViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet,
                    ):
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated, IsSameCompanyUser]

    def get_queryset(self):
        user = self.request.user
        return Supply.objects.select_related('supplier__company').filter(supplier__company_id=user.company_id)


@extend_schema(
    tags=['Products'],
    request=ProductSerializer,
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSameCompanyUser]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        user = self.request.user
        return Product.objects.select_related('storage__company').filter(storage__company_id=user.company_id)




