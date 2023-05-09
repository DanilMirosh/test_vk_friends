from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Класс модели для корректного отображения полей пользователя в админ панели"""
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Особые даты', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
