from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserCustom, UserProfile


class UserAdminCustom(UserAdmin):
    list_display = ['email','username','is_active','is_staff','is_superuser','get_groups']
    readonly_fields = ('last_login','created_at')
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = "Groups"
    fieldsets = (
        (None, {
            "fields": (
                'password','email','username'
            ),
        }),
        ('Activated', {
            "fields": (
                'last_login','created_at'
            ),
        }),

        ('Authorize', {
            "fields": (
                'is_active','is_staff','is_superuser'
            ),
        }),
        ('Permissions', {
            "fields": (
                'groups','user_permissions',
            ),
        }),
    )
    


admin.site.register(UserCustom,UserAdminCustom)    
admin.site.register(UserProfile)    






