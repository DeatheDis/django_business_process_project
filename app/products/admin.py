from django.contrib import admin
from .models import Supplier, Product, SupplyProduct, Supply


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inn', 'company')
    list_filter = ('company',)
    search_fields = ('title', 'inn')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'storage', 'quantity', 'purchase_price')
    list_filter = ('storage',)
    search_fields = ('title',)
    readonly_fields = ('quantity',)


class SupplyProductInline(admin.TabularInline):
    model = SupplyProduct
    extra = 0


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'delivery_date')
    list_filter = ('supplier', 'delivery_date')
    inlines = [SupplyProductInline]
