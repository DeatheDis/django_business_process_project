from django.urls import include, path
from rest_framework import routers
from .views import SupplierViewSet, SupplyViewSet, ProductViewSet


supplier_list = SupplierViewSet.as_view({'get': 'list'})
supplier_create = SupplierViewSet.as_view({'post': 'create'})
supplier_update = SupplierViewSet.as_view({'put': 'update'})
supplier_delete = SupplierViewSet.as_view({'delete': 'destroy'})

supply_list = SupplyViewSet.as_view({'get': 'list'})
supply_create = SupplyViewSet.as_view({'post': 'create'})


product_list = ProductViewSet.as_view({'get': 'list'})
product_create = ProductViewSet.as_view({'post': 'create'})


urlpatterns = [
    path('suppliers/list/', supplier_list, name='supplier-list'),
    path('suppliers/create/', supplier_create, name='supplier-create'),
    path('suppliers/<int:pk>/update/', supplier_update, name='supplier-update'),
    path('suppliers/<int:pk>/delete/', supplier_delete, name='supplier-delete'),

    path('supply/list/', supply_list, name='supply_list'),
    path('supply/create/', supply_create, name='supply_create'),

    path('products/<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='product-detail'),
    path('products/list/', product_list, name='product-list'),
    path('products/add/', product_create, name='product-create'),

    ]
