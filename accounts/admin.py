from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'phone', 'is_verified', 'is_app_admin', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_app_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'phone')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'is_app_admin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
