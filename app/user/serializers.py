from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from company.models import Company


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(),
        message='Пользователь с таким email уже существует')])
    is_company_owner = serializers.BooleanField(read_only=True)
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'password',
                  'is_company_owner',
                  'company', ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'],
            password=validated_data['password'],
            is_company_owner=validated_data.get('is_company_owner', False),
            company=validated_data.get('company', None),
        )

        return user
