from django.contrib.auth.models import AbstractUser
from django.db import models


# === Clase que modela el concepto de un usuario ===
class User(AbstractUser):
    is_active = models.BooleanField(
        ('active'),
        default=False,
        help_text=('Marcar/desmarcar para activar/inactivar cuenta de usuario.'),
    )
    pass

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            ("crear_usuario", "crear_usuario"),
            ("editar_usuario", "editar_usuario"),
            ("agregrar_usuario_proyecto", "agregrar_usuario_proyecto"),
            ("eliminar_usuario", "eliminar_usuario"),
            ("crear_rol", "crear_rol"),
            ("eliminar_rol", "eliminar_rol"),
            ("asignar_rol", "asignar_rol"),
            ("ver_rol", "ver_rol"),
            ("ver_usuarios", "ver_usuarios"),
            ("listar_rol", "listar_rol"),
            ("editar_rol", "editar_rol"),
            ("agregar_usuario_fase", "agregar_usuario_fase"),
            ("quitar_usuario_proyecto", "quitar_usuario_proyecto"),
            ("quitar_usuario_fase", "quitar_usuario_fase"),
            ("mensaje_eliminar", "mensaje_eliminar"),
            ("mensaje_editar", "mensaje_editar"),
            ("ver_mensaje", "ver_mensaje"),
        ]

    def __str__(self):
        """
        **Función para asignar un alias al modelo Usuario**<br/>
        **:return:** el nombre usuario<br/>
        """
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super(User, self).save(*args, **kwargs)

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)