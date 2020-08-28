from django.db import models
from apps.fase.models import Fase
import datetime
import random
import string

from apps.item.models import Item

linea_estado = [('Abierta', 'Abierta'),
                ('Cerrada', 'Cerrada'),
                ('Rota', 'Rota')
                ]


def random_id(lenght=9):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(lenght))


# === Clase que modela el concepto de una linea base para las fases de un proyecto ===
class LineaBase(models.Model):
    # 1. **identificador**: se asigna un identificador unico en el sistema para dicha fase.<br/>
    # 2. **descripción**: Campo para describir brevemente y registrar las informaciónes respecto a una linea base.<br/>
    # 3. **fecha creación**: atributo que almacena la fecha de creación de una linea base.<br/>
    # 4. **estado**: atributo que registra los estados de una linea base.<br/>
    # 5. **fase**: relación que establece una linea base con su fase correspondiente.<br/>
    # 6. **items**: relación que almacena los items con la linea base.<br/>
    identificador = models.CharField(max_length=9, default=random_id, editable=False)
    descripcion = models.TextField(default=None, null=True)
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=linea_estado, default='Abierta')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, default=None, null=True)
    items = models.ManyToManyField(Item, blank=True, related_name="LineaBase")

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            ("crear_linea_base", "crear_linea_base"),
            ("cerrar_linea_base", "cerrar_linea_base"),
            ("ver_linea_base", "ver_linea_base"),
            ("editar_linea_base", "editar_linea_base"),
            ("agregar_item_linea_base", "agregar_item_linea_base"),
            ("quitar_item_linea_base", "quitar_item_linea_base"),
            ("listar_item_linea_base", "listar_item_linea_base"),
            ("estado_linea_base", "estado_linea_base"),
        ]
        verbose_name = 'Linea Base'
        verbose_name_plural = 'Lineas Bases'

    def __str__(self):
        """
        **Función para asignar un alias al modelo linea base**<br/>
        **:return:** el nombre linea base<br/>
        """
        return self.identificador

# el random se ocupa de generar un codigo alganumerico aleatorio a cada linea base creada
# **Volver atras** : [[apps.py]]

# **Ir a la documentación del modelo linea base** : [[models.py]]

# === Indice de la documentación de la Aplicación linea base  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)