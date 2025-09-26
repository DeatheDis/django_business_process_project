from django.db import models


class Storage(models.Model):
    address = models.CharField(unique=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True)
