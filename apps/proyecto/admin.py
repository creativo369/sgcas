# === Código fuente que registra la aplicación Proyecto en Django ===
from django.contrib import admin
from .models import Proyecto
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProyectoResource(resources.ModelResource):
    class Meta:
        model = Proyecto


class ProyectoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['descripcion']
    list_display = ('gerente', 'descripcion', 'fecha_creacion', 'ultima_modificacion', 'estado',)
    resource_class = ProyectoResource


# Registra la aplicación en Django
admin.site.register(Proyecto, ProyectoAdmin)

# **Ir a la documentación del registro de la Aplicación en Django** :[[apps.py]]

# **Ir al final de la documentación** : [[views.py]]

# === Indice de la documentación de la Aplicación Proyecto  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>


# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)

