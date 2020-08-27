from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['username']
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active')
    resource_class = UserResource


admin.site.register(User, UserAdmin)
