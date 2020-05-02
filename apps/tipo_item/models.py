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

    class Meta:
        permissions = [
            ("Can add tipo de item", "Puede crear un tipo de item"),
            ("Can change tipo de item", "Puede editar el tipo de item"),
            ("Can delete tipo de item", "Puede eliminar tipo de item"),
            ("Can view tipo de item", "Puede visualizar tipo de item"),
        ]