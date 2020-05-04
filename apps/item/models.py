from django.db import models
from django.contrib.auth.models import User
import datetime

from apps.fase.models import Fase
from apps.tipo_item.models import TipoItem
# **Estados existentes de un item**
"""
1.En Desarrollo : el item se encuentra disponible para su edición 
2.Aprobado      : el item se encuentra aprobado
3.Desactivado   : el item se encuentra desactivado 
4.Revisión      : el item se encuentra en estado de revisión par su posterior aprobación
5.LineaBase     : el item se encuentra en una linea base 
"""
item_estado = [
    ('Desarrollo', 'Desarrollo'),
    ('Aprobado', 'Aprobado'),
    ('Desactivado', 'Desactivado'),
    ('Revision', 'Revisión'),
    ('LineaBase', 'Línea base'),
]


# === Clase que modela el concepto de un comite para los proyectos ===
class Item(models.Model):
    # 1. **nombre**: Campo para dar asignar un nombre al item.<br/>
    # 2. **descripción**: Campo para describir brevemente información respecto al item.<br/>
    # 3. **fecha_creacion**: campo para registrar la fecha de creación de un item.<br/>
    # 3. **estado**: campo que registra los distintos estados que pueda tener un item.<br/>
    # 3. **costo**: campo que registra el costo de un item.<br/>
    # 3. **usuarios_a_cargo**: Relación de MuchosAmuchos con los miembros de una para estar a cargo de ese item.<br/>
    # 3. **archivo**: campo que almacena un archivo adjunto al item.<br/>
    # 3. **fase**: Relación con la fase donde va a corresponder.<br/>
    # 3. **tipo_item**: campo donde asigna un tipo de item .<br/>
    # 3. **boolean**: atributo boolean.<br/>
    # 3. **char**: atributo char.<br/>
    # 3. **date**: atributo date.<br/>
    # 3. **numerico**: atributo numerico.<br/>
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=item_estado, default='Desarrollo')
    costo = models.PositiveIntegerField()
    usuarios_a_cargo = models.ManyToManyField(User, blank=True)
    archivo = models.FileField(null=True, blank=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, null=True)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True, default='')
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=100, default='', blank=True)
    date = models.DateField(null=True, blank=True)
    numerico = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """
        **Función para asignar un alias al modelo item**<br/>
        **:return:** el nombre comité<br/>
        """
        return self.nombre

# **Volver atras** : [[forms.py]]

# **Ir a la documentación de pruebas unitarias del modulo item** : [[tests.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
