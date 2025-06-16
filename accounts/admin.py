from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'first_name', 'last_name', 'role',
        'is_email_verified', 'is_staff', 'is_active'
    )
    list_filter = (
        'role', 'is_email_verified', 'is_staff', 'is_active'
    )
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Verification', {'fields': ('is_email_verified',)}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'role',
                'password1', 'password2',
                'is_staff', 'is_active', 'is_email_verified'
            )
        }),
    )

    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(CustomUser, CustomUserAdmin)
