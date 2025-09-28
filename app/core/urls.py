from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


BASE_API_V1_PREFIX = 'api/v1'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path(f'{BASE_API_V1_PREFIX}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{BASE_API_V1_PREFIX}/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path(f'{BASE_API_V1_PREFIX}/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path(f'{BASE_API_V1_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{BASE_API_V1_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'{BASE_API_V1_PREFIX}/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(f'{BASE_API_V1_PREFIX}/', include('user.urls')),
    path(f'{BASE_API_V1_PREFIX}/', include('company.urls')),
]
