from django.contrib.auth.models import Group
from django.db import models
from apps.fase.models import Fase
from apps.usuario.models import User


class Rol(models.Model):
    nombre = models.CharField(max_length=50, default="")
    group = models.OneToOneField('auth.Group', unique=True, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, default=None, blank=True, null=True)
    usuarios = models.ManyToManyField(
        User,
        blank=True,
    )

    def __str__(self):
        return self.nombre
