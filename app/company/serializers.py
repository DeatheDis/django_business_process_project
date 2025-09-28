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


