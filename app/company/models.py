from django.db import models


class Company(models.Model):
    inn = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=False)
    owner = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='company_owner')

    def __str__(self):
        return self.title

    objects = models.Manager()
