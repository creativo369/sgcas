# === Código fuente que registra la aplicación item en Django ===

from django.contrib import admin
from .models import Item
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item


class ItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'descripcion', 'fecha_creacion', 'estado',)
    resource_class = ItemResource


# Registra la aplicación en Django
admin.site.register(Item,ItemAdmin)

# **Ir a la documentación del registro de la Aplicación en Django** :[[apps.py]]

# **Ir al final de la documentación** : [[views.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
