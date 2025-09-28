from rest_framework import serializers
from company.models import Company
from .models import Storage


class CompanyForStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'title', 'inn']


class StorageSerializer(serializers.ModelSerializer):
    company = CompanyForStorageSerializer(read_only=True)

    class Meta:
        model = Storage
        fields = ['id', 'address', 'company']
        read_only_fields = ['id', 'company']

    def validate(self, attrs):
        request = self.context.get('request')
        view = self.context.get('view')

        if request and getattr(view, 'action', None) == 'create':
            user = request.user
            if not user.company_id:
                raise serializers.ValidationError('Пользователь не привязан к компании')
            if Storage.objects.filter(company_id=user.company_id).exists():
                raise serializers.ValidationError('У вашей компании уже есть склад')
        return attrs
