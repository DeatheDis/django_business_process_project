from rest_framework import serializers
from .models import Supplier, Product, Supply, SupplyProduct


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'title',
            'inn'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['company_id'] = user.company_id
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id',
                  'title',
                  'quantity',
                  'purchase_price',
                  'sale_price',
                  'storage']
        read_only_fields = ['id',
                            'quantity',
                            'storage']

    def validate_title(self, title):
        user = self.context['request'].user

        if Product.objects.filter(
                storage__company_id=user.company_id,
                title=title
        ).exists():
            raise serializers.ValidationError(
                'Товар с таким названием уже существует в вашем складе'
            )

        return title

    def create(self, validated_data):
        user = self.context['request'].user

        if not user.company.storage:
            raise serializers.ValidationError(
                'У вас нет склада, для добавления товаров'
            )

        validated_data['storage'] = user.company.storage
        validated_data['quantity'] = 0
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            raise serializers.ValidationError('Изменение возможно, только через поставки')
        if 'storage' in validated_data and instance.storage_id != validated_data['storage'].id:
            raise serializers.ValidationError('Нельзя изменить склад')
        return super().update(instance, validated_data)


class SupplyProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = SupplyProduct
        fields = ['product',
                  'product_title',
                  'quantity']


class SupplySerializer(serializers.ModelSerializer):
    items = SupplyProductSerializer(many=True, write_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    products = SupplyProductSerializer(source='items', many=True, read_only=True)

    class Meta:
        model = Supply
        fields = ['id',
                  'supplier',
                  'delivery_date',
                  'items',
                  'products']
        read_only_fields = ['id']

    def validate_supplier(self, supplier):
        user = self.context['request'].user
        if supplier.company_id != user.company_id:
            raise serializers.ValidationError('Поставщик не принадлежит вашей компании.')
        return supplier

    def validate(self, attrs):
        items = attrs.get('items', [])
        user_company_id = self.context['request'].user.company_id

        if not items:
            raise serializers.ValidationError('Нужен список товаров с количеством')

        product_ids = []
        for item in items:
            if item['quantity'] <= 0:
                raise serializers.ValidationError('Количество товаров не может быть отрицательным')

            product = item['product']
            product_ids.append(product.id)

            if product.storage.company_id != user_company_id:
                raise serializers.ValidationError(
                    f'Товар "{product.title}" не принадлежит вашей компании'
                )

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                'Один товар не может быть в одной поставке несколько раз.'
            )

        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        supply = Supply.objects.create(**validated_data)

        supply_products = []

        for item in items_data:
            product = item['product']
            supply_products.append(
                SupplyProduct(
                    supply=supply,
                    product=product,
                    quantity=item['quantity']
                )
            )
            product.quantity += item['quantity']

        SupplyProduct.objects.bulk_create(supply_products)
        Product.objects.bulk_update(
            [item['product'] for item in items_data],
            ['quantity']
        )
        return supply
