from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model=CustomUser
    list_display=('email','first_name','last_name','role','is_staff','is_active')
    list_filter=('role','is_staff','is_active')
    ordering=('email',)
    search_fields=('email','first_name','last_name')
    fieldsets=(
        (None,{'fields':('email','password')}),
        ('Permissions',{'fields':('role','is_staff','is_active','is_superuser')}), #optional -> 'groups','user_permissions'
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','first_name','last_name','role','password1','password2','is_staff','is_active')
        }),
    )

    def has_change_permission(self, request, obj = None):
        return True

admin.site.register(CustomUser,CustomUserAdmin)
