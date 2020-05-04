from django.db import models
from multiselectfield import MultiSelectField
# === Atributos de un tipo de item ===
ATTRIBUTES = [
    ('Boolean', 'Boolean'),
    ('Char', 'Char'),
    ('Date', 'Date'),
    ('Numerico', 'Numerico'),
]


# === Clase que modela el concepto de un TipoItem ===
class TipoItem(models.Model):
    # 1. **nombre**: asignamos un nombre al tipo de item<br/>
    # 2. **descripción**: campo que almacena la descripción del tipo de item.<br/>
    # 3. **atributos**: campo para seleccionar los atributos los tipos de items.<br/>
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    atributos = MultiSelectField(choices=ATTRIBUTES)

    def __str__(self):
        return self.nombre
# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
