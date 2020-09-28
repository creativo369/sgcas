from django.db import models
from apps.usuario.models import User
from apps.proyecto.models import Proyecto


# === Clase que modela el concepto de un comite para los proyectos ===
class Comite(models.Model):
    # 1. **nombre**: Campo para dar asignar un nombre al comité.<br/>
    # 2. **descripción**: Campo para describir brevemente las responsabilidades e información.<br/>
    # 3. **miembros**: Relación de MuchosAmuchos con los miembros de un proyecto.<br/>
    # 4. **proyecto**: Relación del comite con un proyecto.<br/>

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    miembros = models.ManyToManyField(User, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        """
        **Función para asignar un alias al modelo Comité**<br/>
        **:return:** el nombre comité<br/>
        """
        return self.nombre

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            # ("crear_comite", "crear_comite"),
            # ("eliminar_comite", "eliminar_comite"),
            # ("ver_comite", "ver_comite"),
            # ("editar_comite", "editar_comite"),
            # ("listar_comite", "listar_comite"),
            # ("agregar_comite_proyecto", "agregar_comite_proyecto"),
            # ("quitar_comite_proyecto", "quitar_comite_proyecto"),
            # ("agregar_usuario_comite", "agregar_usuario_comite"),
            # ("quitar_usuario_comite", "quitar_usuario_comite"),
            ("crear_comite", "Puede crear comite"),
            ("crear_solicitud", "Puede crear solicitud"),
            ("editar_comite", "Puede editar comite"),
            ("ver_comite", "Puede ver comite"),
            ("ver_solicitud", "Puede ver solicitud"),
            ("eliminar_comite", "Puede eliminar comite"),
        ]

        verbose_name = 'Comité'
        verbose_name_plural = 'Comites'

# **Volver atras** : [[forms.py]]

# **Ir a la documentación de pruebas unitarias del modulo comité** : [[tests.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
