from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_company_owner', 'company', 'is_active', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'company__title')
    list_filter = ('is_company_owner', )

