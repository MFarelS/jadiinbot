from django.contrib import admin
from main.models import User, Session

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions']

admin.site.register(Session)
admin.site.register(User, UserAdmin)
