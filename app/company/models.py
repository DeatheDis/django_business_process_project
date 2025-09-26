from django.db import models


class Company(models.Model):
    inn = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
