# === Código fuente que registra la aplicación fase en Django ===
from django.contrib import admin
from .models import Fase
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class FaseResource(resources.ModelResource):
    class Meta:
        model = Fase


class FaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'descripcion', 'fecha_creacion', 'estado', 'proyecto',)
    resource_class = FaseResource


# Registra la aplicación en Django
admin.site.register(Fase, FaseAdmin)


# **Ir a la documentación del registro de la Aplicación en Django** :[[apps.py]]

# **Ir al final de la documentación** : [[views.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
