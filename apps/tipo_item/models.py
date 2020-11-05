from django.db import models
from apps.fase.models import Fase
from apps.proyecto.models import Proyecto
from multiselectfield import MultiSelectField

# === Atributos de un tipo de item ===
ATTRIBUTES = [
    ('Boolean', 'Boolean'),
    ('Char', 'Char'),
    ('Date', 'Date'),
    ('Numerico', 'Numerico'),
]


# === Clase que modela el concepto de un TipoItem ===
class TipoItem(models.Model):
    # 1. **nombre**: asignamos un nombre al tipo de item<br/>
    # 2. **descripción**: campo que almacena la descripción del tipo de item.<br/>
    # 3. **atributos**: campo para seleccionar los atributos los tipos de items.<br/>
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    atributos = MultiSelectField(choices=ATTRIBUTES)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True) # El proyecto origen que pertenece el tipo de item

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de los permisos por defecto que  trae django
        permissions = [
            # ("crear_tipo_item", "crear_tipo_item"),
            # ("adjuntar_tipo_item", "adjuntar_tipo_item"),
            # ("listar_tipo_item", "listar_tipo_item"),
            # ("editar_tipo_item", "editar_tipo_item"),
            # ("eliminar_tipo_item", "eliminar_tipo_item"),
            # ("importar_tipo_item", "importar_tipo_item"),
            # ("ver_tipo_item", "ver_tipo_item"),

            ("crear_tipo_item", "Puede crear tipo item"),
            ("editar_tipo_item", "Puede editar tipo item"),
            ("listar_tipo_item", "Puede listar tipo item"),
            ("ver_tipo_item", "Puede ver tipo item"),
            ("eliminar_tipo_item", "Puede eliminar tipo item"),
            ("adjuntar_tipo_item", "Puede adjuntar tipo item"),
            ("importar_tipo_item", "Puede importar tipo item"),

        ]

    def __str__(self):
        return self.nombre


class ItemImportado(models.Model):
    id_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE, blank=True, null=True)
    proyecto_destino = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True)


# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
