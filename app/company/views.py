from user.serializers import UserSerializer
from .permissions import IsCompanyOwner, CanCreateCompany
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from .serializers import CompanySerializer, EmployeeSerializer
from company.models import Company
from user.models import User

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)


@extend_schema(
    tags=['Companies'],
    request=CompanySerializer,
)
class CompanyViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Company.objects.select_related('owner', 'storage').all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), CanCreateCompany()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        company = serializer.save(owner=self.request.user)
        user.company = company
        user.is_company_owner = True
        user.save(update_fields=['company', 'is_company_owner'])


@extend_schema(
    tags=['Companies'],
    request=CompanySerializer,
)
class MyCompanyView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Company.objects.none()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]

    def get_object(self):
        user = self.request.user
        company = getattr(user, 'company', None)
        if not company:
            raise NotFound('У вас нет компании.')
        if company.owner_id != user.id:
            raise PermissionDenied('Только владелец может управлять компанией.')
        return company

    def perform_destroy(self, instance):
        from user.models import User
        User.objects.filter(company_id=instance.id).update(company=None)
        owner = instance.owner
        owner.is_company_owner = False
        owner.company = None
        owner.save(update_fields=['is_company_owner', 'company'])
        instance.delete()

    @extend_schema(
        tags=['Employees'],
        examples=[
            OpenApiExample('Пример ответа', response_only=True,
                           value=[{"id": 12,
                                   "email": "example@example.com"},
                                  {"id": 34,
                                   "email": "example@example.com"}]
                           )
        ]
    )
    def employees(self, request, pk=None):
        company = self.get_object()
        data = list(User.objects.filter(company_id=company.id).values('id', 'email'))
        return Response(data)

    @extend_schema(
        tags=['Employees'],
        request=EmployeeSerializer,
    )
    def add_employee(self, request):
        company = self.get_object()
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        email = serializer.validated_data.get('email')

        target = None
        if user_id is not None:
            target = User.objects.filter(id=user_id).first()
        elif email is not None:
            target = User.objects.filter(email=email).first()

        if not target:
            raise NotFound('Пользователь не найден')

        if target.id == company.owner_id:
            raise ValidationError('Вы и так являетесь сотрудником компании')

        if target.company_id is not None:
            raise ValidationError('Пользователь уже состоит в компании.')

        if getattr(target, 'is_company_owner', False):
            raise ValidationError('Пользователь является владельцем компании')

        target.company_id = company.id
        target.save(update_fields=['company'])

        return Response('Сотрудник добавлен')

    @extend_schema(
        tags=['Employees'],
    )
    def employees_remove(self, request, pk=None, user_id=None):
        company = self.get_object()

        if int(user_id) == company.owner_id:
            raise PermissionDenied('Нельзя удалить владельца')

        target = User.objects.filter(id=user_id, company_id=company.id).first()
        if not target:
            raise NotFound('Сотрудник не найден в этой компании')

        target.company = None
        target.save(update_fields=['company'])

        return Response('Сотрудник удалён')
