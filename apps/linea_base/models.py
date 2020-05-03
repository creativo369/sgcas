from django.db import models
from django.contrib.auth.models import User
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


class LineaBase(models.Model):
    identificador = models.CharField(max_length=9, default=random_id, editable=False)
    descripcion = models.TextField(default=None, null=True)
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=linea_estado, default='Abierta')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, default=None, null=True)
    items = models.ManyToManyField(Item, blank=True, related_name="LineaBase")

    def __str__(self):
        return self.identificador

# el random se ocupa de generar un codigo alganumerico aleatorio a cada linea base creada
