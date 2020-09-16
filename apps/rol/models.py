from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from apps.fase.models import Fase
from apps.usuario.models import User
from django.core.exceptions import ValidationError


class Rol(models.Model):
    nombre = models.CharField(max_length=50, default="")
    group = models.OneToOneField('auth.Group', unique=True, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, default=None, blank=True, null=True)
    usuarios = models.ManyToManyField(
        User,
        blank=True,
    )

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            ("crear_rol", "Puede crear rol"),
            ("editar_rol", "Puede editar rol"),
            ("listar_rol", "Puede listar rol"),
            ("eliminar_rol", "Puede eliminar rol"),
            ("asignar_rol", "Puede asignar rol"),
            # === PERMISOS SOBRE LOS ROLES DE SISTEMA ===
            ("crear_rol_sistema", "Puede crear rol sistema"),
            ("editar_rol_sistema", "Puede editar rol sistema"),
            ("gestion_rol_sistema", "Puede gestionar rol sistema"),
            ("listar_rol_sistema", "Puede listar rol sistema"),
            ("eliminar_rol_sistema", "Puede eliminar rol sistema"),
            ("asignar_rol_sistema", "Puede asignar rol sistema"),

        ]
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if Rol.objects.filter(Q(id=self.id) &
            Q(usuarios__in=User.objects.all().exclude(username='AnonymousUser').exclude(is_superuser=True))).exists():
            raise ValidationError('Este rol esta asignado a un usuario') 
        else:
                super(Rol, self).delete(*args, **kwargs)
