from django.db import models
from multiselectfield import MultiSelectField

ATTRIBUTES = [
    ('Boolean', 'Boolean'),
    ('Char', 'Char'),
    ('Date', 'Date'),
    ('Numerico', 'Numerico'),
]

class TipoItem(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    atributos = MultiSelectField(choices=ATTRIBUTES)

    def __str__(self):
        return self.nombre
