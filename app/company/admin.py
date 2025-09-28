from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'inn', 'title', 'owner')
    list_display_links = ('id', 'inn', 'title')
    search_fields = ('inn', 'title', 'owner__email')
    list_filter = ('inn', 'title')
