from django.urls import path
from .views import StorageViewSet

storage_detail = StorageViewSet.as_view({'get': 'retrieve'})
storage_create = StorageViewSet.as_view({'post': 'create'})
storage_update = StorageViewSet.as_view({'put': 'update'})
storage_delete = StorageViewSet.as_view({'delete': 'destroy'})

urlpatterns = [
    path('storage/create/', storage_create, name='storage-create'),
    path('storage/<int:pk>/', storage_detail, name='storage-detail'),
    path('storage/update/<int:pk>/', storage_update, name='storage-update'),
    path('storage/delete/<int:pk>/', storage_delete, name='storage-delete'),
]
