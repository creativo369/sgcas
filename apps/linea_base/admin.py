from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import LineaBase


class LineaBaseResource(resources.ModelResource):
    class Meta:
        model = LineaBase


class LineaBaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['descripcion']
    list_display = ('descripcion', 'fecha_creacion', 'estado', 'fase',)
    resource_class = LineaBaseResource


admin.site.register(LineaBase, LineaBaseAdmin)

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)