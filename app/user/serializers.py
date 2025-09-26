from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'password',
                  'is_company_owner',
                  'company', ]

    extra_kwargs = {'username': {'required': False},
                    'email': {'required': True}
                    }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'],
            password=validated_data['password'],
            is_company_owner=validated_data.get('is_company_owner', False),
            company=validated_data.get('company', None),
        )

        return user
