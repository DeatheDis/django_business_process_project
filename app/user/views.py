from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)


@extend_schema(
    tags=['Users'],
    request=UserSerializer,
    description='Регистрация нового пользователя',
    auth=[],
    examples=[
        OpenApiExample(
            'Register without company',
            value={
                "username": "Test",
                "email": "test@test.com",
                "password": "123456",
                "is_company_owner": False,
                "company": None
            }
        ),
    ]
)
class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
