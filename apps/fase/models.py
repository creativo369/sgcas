from django.db import models
from django.contrib.auth.models import User
from apps.proyecto.models import Proyecto
import datetime

fase_estado = [('Abierta', 'Abierta'),
               ('Cerrada', 'Cerrada')
               ]


class Fase(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=fase_estado, default='Abierta')
    miembros = models.ManyToManyField(User, blank=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)
