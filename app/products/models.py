from django.core.validators import MinValueValidator
from django.db import models


class Supplier(models.Model):
    company = models.ForeignKey('company.Company',
                                on_delete=models.CASCADE,
                                related_name='suppliers')
    title = models.CharField(max_length=100)
    inn = models.CharField(max_length=12, unique=True)

    class Meta:
        unique_together = ('company', 'title')
        ordering = ['title']

    def __str__(self):
        return self.title

    objects = models.Manager()


class Product(models.Model):
    title = models.CharField(max_length=100)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=12)
    sale_price = models.DecimalField(decimal_places=2, max_digits=12)
    quantity = models.PositiveIntegerField(default=0)
    storage = models.ForeignKey('storage.Storage',
                                on_delete=models.CASCADE,
                                related_name='products')

    class Meta:
        unique_together = ('storage', 'title')
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.quantity}'

    objects = models.Manager()


class Supply(models.Model):
    supplier = models.ForeignKey('Supplier',
                                 on_delete=models.CASCADE,
                                 related_name='supplies')
    delivery_date = models.DateField()
    products = models.ManyToManyField(
        'Product',
        through='SupplyProduct',
        related_name='supplies'
    )

    objects = models.Manager()


class SupplyProduct(models.Model):
    supply = models.ForeignKey('Supply', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='supply_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('supply', 'product')

    objects = models.Manager()
