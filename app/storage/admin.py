from django.contrib import admin
from .models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'company')
    list_display_links = ('id', 'address', 'company')
    search_fields = ('address', 'company__title', 'company__inn')
    list_filter = ('company', )
