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

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 0.admin   : [[admin.py]]<br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)