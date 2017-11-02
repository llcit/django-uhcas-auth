from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UHCASUser

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UHCASUserInline(admin.StackedInline):
    model = UHCASUser
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UHCASUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
