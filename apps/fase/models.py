from django.db import models
from apps.usuario.models import User
from apps.proyecto.models import Proyecto
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime

# === Estados de una fase ===
fase_estado = [('Abierta', 'Abierta'),
               ('Cerrada', 'Cerrada')
               ]


# === Clase que modela el concepto de una fase para los proyectos ===
class Fase(models.Model):
    # 1. **nombre**: Campo para dar asignar un nombre a la fase.<br/>
    # 2. **descripción**: Campo para describir brevemente las información referente a una instancia del modelo fase.<br/>
    # 3. **fecha_creacion**: información que registra la fecha de creación.<br/>
    # 3. **estado**: atributo que registra los estados de la fase.<br/>
    # 3. **miembros**: Relación de MuchosAmuchos con los miembros de un proyecto a la fase.<br/>
    # 4. **proyecto**: Relación de la fase con un proyecto.<br/>
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=fase_estado, default='Abierta')
    miembros = models.ManyToManyField(User, blank=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            # ("crear_fase", "crear_fase"),
            # ("aprobar_fase", "aprobar_fase"),
            # ("editar_fase", "editar_fase"),
            # ("eliminar_fase", "eliminar_fase"),
            # ("listar_fase", "listar_fase"),
            # ("cambio_estado_fase", "cambio_estado_fase"),
            # ("ver_fase", "ver_fase"),
            # ("detalles_fase", "detalles_fase"),

            ("crear_fase", "Puede crear fase"),
            ("editar_fase", "Puede editar fase"),
            ("gestion_fase", "Puede ver gestion de fase"),
            ("detalles_fase", "Puede ver los detalles de fase"),
            ("eliminar_fase", "Puede eliminar fase"),
            ("listar_fase", "Puede listar fase"),
            ("cambio_estado_fase", "Puede cambiar estado fase"),
        ]

        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'


    def __str__(self):
        """
        **Función para asignar un alias al modelo Comité**<br/>
        **:return:** el nombre fase<br/>
        """
        return '{}'.format(self.nombre)

# **Volver atras** : [[forms.py]]

# **Ir a la documentación de pruebas unitarias del modulo fase** : [[tests.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)