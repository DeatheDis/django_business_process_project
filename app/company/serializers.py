from rest_framework import serializers
from .models import Company
from user.models import User
from storage.models import Storage


class OwnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class StorageCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'address']


class CompanySerializer(serializers.ModelSerializer):
    owner = OwnerCompanySerializer(read_only=True)
    storage = StorageCompanySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id',
                  'inn',
                  'title',
                  'owner',
                  'storage', ]


class EmployeeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        if not attrs.get('user_id') and not attrs.get('email'):
            raise serializers.ValidationError('Укажите user_id или email.')
        return attrs
