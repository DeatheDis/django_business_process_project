from rest_framework import serializers
from .models import Company
from user.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CompanySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id',
                  'inn',
                  'title',
                  'owner',]

    def validate(self, attrs):
        request = self.context.get('request')
        view = self.context.get('view')
        if request and request.user.is_authenticated and getattr(view, 'action', None) == 'create':
            if Company.objects.filter(owner=request.user).exists():
                raise serializers.ValidationError('Нельзя создать компанию: вы уже являетесь владельцем компании.')
        return attrs
