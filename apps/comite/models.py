from django.db import models
from django.contrib.auth.models import User

from apps.proyecto.models import Proyecto


class Comite(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    miembros = models.ManyToManyField(User, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.nombre
