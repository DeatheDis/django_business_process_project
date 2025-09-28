from django.db import models


class Storage(models.Model):
    address = models.CharField(max_length=255, unique=True)
    company = models.OneToOneField('company.Company', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='storage')
