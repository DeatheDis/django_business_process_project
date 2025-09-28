from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StorageViewSet

router = DefaultRouter()
router.register('storage', StorageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]