from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password', 'is_company_owner', 'company', 'is_active', 'is_superuser')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'company')
    list_filter = ('email', 'company')
