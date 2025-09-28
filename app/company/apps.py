from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company'
    verbose_name = 'Компания'
    verbose_name_plural = 'Компании'
