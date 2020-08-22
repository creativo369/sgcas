from django.db import models

from apps.usuario.models import User
import datetime
from django.core.exceptions import ValidationError

# **Diccionario para establecer los estados de un proyecto**
estado_proyecto = [
    ('Pendiente', 'Pendiente'),
    ('Iniciado', 'Iniciado'),
    ('Cancelado', 'Cancelado'),
    ('Finalizado', 'Finalizado'),
]


# **Clase que modela el concepto de Proyecto**
class Proyecto(models.Model):
    # 1. **user**: Campo para dar asignar implicitamente al gerente como creador del proyecto.<br/>
    # 2. **nombre**: definir el nombre del proyecto.<br/>
    # 3. **descripción**: describimos brevemente información acerca del proyecto.<br/>
    # 4. **fecha_creación**: establecemos la fecha de creación.<br/>
    # 5. **ultima_modificación**: atributo que llevara el registro de la ultima modificación de un proyecto.<br/>
    # 6. **estado**: atributo que llevara el registro por los diferentes estados que pasara el proyecto.<br/>
    # 7. **slug**: atributo que establece que el proyecto sea unico.<br/>
    # 8. **miembros**: cambio que establece la relación de un proyecto y miembros ( guarda la asignación de los miembros).<br/>

    gerente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gerente')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=30, choices=estado_proyecto, default="Pendiente")
    slug = models.CharField('Slug', max_length=100, blank=False, null=False)
    miembros = models.ManyToManyField(User, blank=True)

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            ("crear_proyecto", "crear_proyecto"),
            ("iniciar_proyecto", "iniciar_proyecto"),
            ("finalizar_proyecto", "finalizar_proyecto"),
            ("cancelar_proyecto", "cancelar_proyecto"),
            ("ver_proyecto", "ver_proyecto"),
            ("eliminar_proyecto", "eliminar_proyecto"),
            ("editar_proyecto", "editar_proyecto"),
            ("detalles_proyecto", "detalles_proyecto"),
        ]
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        """
        Función que retorna el nombre del modelo a una instancia llamada "proyecto"<br/>
        :return: nombre del modelo a una instancia <br/>
        """
        return self.nombre

    def validate_unique(self, exclude=None):
        """
        Función que valida que el nombre de un proyecto sea unico.<br/>
        **:param exclude:** None<br/>
        **:return:** Mensaje de Validación<br/>
        """
        if Proyecto.objects.filter(nombre=self.nombre).exclude(pk=self.id).exists():
            raise ValidationError("Un proyecto con el mismo título ya se encuentra registrado")

    def save(self, *args, **kwargs):
        """
        Función que guarda el proyecto en la base de datos como unico.<br/>
        **:param args:**<br/>
        **:param kwargs:**<br/>
        **:return:** Un string que va ser unico en nuestra base de datos<br/>
        """
        self.validate_unique()
        self.slug = self.nombre.replace(" ", "_").lower()
        super(Proyecto, self).save(*args, **kwargs)

# **Volver atras** : [[forms.py]]

# **Ir a la documentación del tests de la Aplicación** :[[tests.py]]

# === Indice de la documentación de la Aplicación Proyecto  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
