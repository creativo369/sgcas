from django.db import models
from apps.usuario.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
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
]


# === Clase que modela el concepto de un comite para los proyectos ===
class Item(models.Model):
    # 1. **nombre**: Campo para dar asignar un nombre al item.<br/>
    # 2. **descripción**: Campo para describir brevemente información respecto al item.<br/>
    # 3. **fecha_creacion**: campo para registrar la fecha de creación de un item.<br/>
    # 4. **estado**: campo que registra los distintos estados que pueda tener un item.<br/>
    # 5. **costo**: campo que registra el costo de un item.<br/>
    # 6. **usuarios_a_cargo**: Relación de MuchosAmuchos con los miembros de una para estar a cargo de ese item.<br/>
    # 7. **archivo**: campo que almacena un archivo adjunto al item.<br/>
    # 8. **fase**: Relación con la fase donde va a corresponder.<br/>
    # 9. **tipo_item**: campo donde asigna un tipo de item .<br/>
    # 10. **boolean**: atributo boolean.<br/>
    # 11. **char**: atributo char.<br/>
    # 12. **date**: atributo date.<br/>
    # 13. **numerico**: atributo numerico.<br/>
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, choices=item_estado, default='Desarrollo')
    en_linea_base = models.BooleanField(default=False)
    costo = models.PositiveIntegerField()
    usuarios_a_cargo = models.ManyToManyField(User, blank=True)
    archivo = models.FileField(null=True, blank=True)
    file_url_cloud = models.CharField(max_length=200, null=True, blank=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, null=True)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True, default='')
    impacto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ### Atributos para tipos de item ###
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=100, default='', blank=True)
    date = models.DateField(null=True, blank=True)
    numerico = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ### Atributos para relaciones ###
    padres = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='padre')
    hijos = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='hijo')
    antecesores = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='antecesor')
    sucesores = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='sucesor')
    ### Atributos para el versionado
    nro_version = models.DecimalField(max_digits=10, decimal_places=1, default=0.1)
    versiones = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    last_release = models.BooleanField(default=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()  # se deshabilita la creacion de permisos por defecto de django
        permissions = [
            # ("crear_item", "crear_item"),
            # ("aprobar_item", "aprobar_item"),
            # ("editar_item", "editar_item"),
            # ("eliminar_item", "eliminar_item"),
            # ("relacionar_item", "relacionar_item"),
            # ("restaurar_item_version", "restaurar_item_version"),
            # ("ver_item", "ver_item"),
            # ("ver_versiones_item", "ver_versiones_item"),
            # ("item_modificar_atributos", "item_modificar_atributos"),
            # ("cambiar_estado_item", "cambiar_estado_item"),
            # ("item_modificar_ti", "item_modificar_ti"),
            # ("item_modificar_atributos_ti", "item_modificar_atributos_ti"),
            # ("item_modificar_import_ti", "item_modificar_import_ti"),
            # ("listar_item_de_fase", "listar_item_de_fase"),
            # ("calcular_impacto", "calcular_impacto"),
            # ("ver_trazabilidad", "ver_trazabilidad"),

            ("crear_item", "Puede crear item"),
            ("editar_item", "Puede editar item"),
            ("listar_item", "Puede listar item"),
            ("ver_item", "Puede ver item"),
            ("eliminar_item", "Puede eliminar item"),
            ("cambiar_estado_item", "Puede cambiar estado item"),
            ("relacion_item", "Puede gestionar relacion de item"),
            ("calcular_impacto", "Puede calcular impacto item"),
            ("ver_trazabilidad", "Puede ver trazabilidad item"),
            ("versiones_item", "Puede versionar item"),
            ("restaurar_item_version", "Puede restaurar version item"),
            ("item_modificar_atributos", "Puede modificar atributos item"),
            ("item_modificar_ti", "Puede modificar TI de item"),
            ("item_modificar_atributos_ti", "Puede modificar atributos ti de item"),
            ("item_modificar_import_ti", "Puede modificar  import ti de item"),
        ]

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

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

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)