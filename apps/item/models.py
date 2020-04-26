from django.db import models
from django.contrib.auth.models import User
import datetime
from apps.tipo_item.models import TipoItem

item_estado = [
    ('Aprobado', 'Aprobado'),
    ('Desactivado', 'Desactivado'),
    ('Revision', 'Revisión'),
    ('Desarrollo', 'Desarrollo'),
    ('LineaBase', 'Línea base'),
]


class Item(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=item_estado, default='Desarrollo')
    costo = models.PositiveIntegerField()
    usuarios_a_cargo = models.ManyToManyField(User, blank=True)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True, default='')
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=10, default='', blank=True)
    date = models.DateField(null=True, blank=True)
    numerico = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# ASIGNACION DE ATRIBUTOS
# Nombre
# Descripcion
# Archivos adjuntos
# Usuario asignado
# Costo
# Relacion (No se contempla para la iteracion 3)

# SE PERMITE LA MODIFICACION DE ATRIBUTOS
# - Nombre
# - Descripcion
# - Usuario encargado
# - Costo
# - Archivos adjuntos

# RF.28: El sistema permite agregar, modificar y visualizar archivos adjuntos.
# RF.29: Permite visualizar nombre, descripción, usuario asignado y tiempo estimado de duración del ítem.
# RF.31: El sistema permite mantener un historial de las modificaciones de un ítem con la posibilidad de re#alizar reversiones a versiones anteriores.
# RF.33: El sistema permite que el usuario determine cuando un ítem está aprobado.
# RF.75: Los costos de los ítems serán expresados en horas estimativas.
# RF.76: El sistema deberá notificar al usuario cuando se le asigne un ítem.
# RF.77: El sistema permite eliminar ítems de las fases de un proyecto.
# RF.84: El versionado de un ítem empieza en el momento de su creación.
# RF.85: Un ítem debe de estar en estado de desarrollo para su desactivación.
# RF.86: Al modificar un ítem aprobado, éste debe de ser nuevamente aprobado.
# RF.90: El formato de fecha del versionado de los ítems es el dd/mm/yyyy.
