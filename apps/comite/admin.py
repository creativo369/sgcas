# === Código fuente que registra la aplicación Comité en Django ===
from django.contrib import admin
from .models import Comite
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ComiteResource(resources.ModelResource):
    class Meta:
        model = Comite


class ComiteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'descripcion', 'proyecto',)
    resource_class = ComiteResource


# Registra la aplicación en Django
admin.site.register(Comite, ComiteAdmin)

# **Ir a la documentación del registro de la Aplicación en Django** :[[apps.py]]

# **Ir al final de la documentación** : [[views.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
