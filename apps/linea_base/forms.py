# === Importamos las librerias necesarias para la implementación de un Formulario ===
from django import forms
from django.db.models import Q
from .models import LineaBase

# === Clase para abstraer en un formulario el registro de un Comité ===
from ..item.models import Item


# ** Formulario para el registro de una linea base **
class LineaBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga desplegar los campos requeridos , los que no se permiten modificar en la plantilla.<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo linea base<br/>
        """
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True

    # **Clase Meta para para el despliegue en una plantilla de los campos necesarios del modelo**
    class Meta:
        model = LineaBase

        fields = [  # campos de mi modelo
            'descripcion',
            'estado',
        ]
        labels = {  # las etiquetas que tendra para visualizarse en el navegador
            'descripcion': 'Descripcion de la Linea Base',
            'estado': 'Estado de la Linea Base',
        }
        widgets = {  # los aparatos o elementos de captura de información del formulario
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Describa la Linea Base',
                                                 'rows': 5,
                                                 'cols': 50}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }


# === Clase para abstraer en un formulario la actualización del estado de una linea base ===
class LineaBaseUpdateEstado(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LineaBaseUpdateEstado, self).__init__(*args, **kwargs)

        if kwargs['instance'].estado=='Abierta':
            linea_base_new =[
                ('Cerrada', 'Cerrada'),                
                ]
            self.fields['estado'].choices=linea_base_new
            
        self.fields['descripcion'].required = False
        self.fields['descripcion'].disabled = True

    class Meta(LineaBaseForm.Meta):
        model = LineaBase


# === Clase para abstraer en un formulario la actualización de una linea base ===
class LineaBaseUpdateForm(LineaBaseForm):

    # Para read-only el field estado
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los campos editables para la acutalización de una linea base<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo linea base<br/>
        """
        super(LineaBaseUpdateForm, self).__init__(*args, **kwargs)
        # fields representa los campos que no son editables de acuerdo al estado de la linea base
        fields = ['estado']
        if 'instance' in kwargs:
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(LineaBaseForm.Meta):
        model = LineaBase

# === Clase para abstraer en un formulario agregar items a una linea base ===
class AgregarItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los campos items que no fueron colocados en una linea base<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo de items que no estan en linea base<br/>
        """
        id_fase = kwargs.pop('id_fase')
        super(AgregarItemsForm, self).__init__(*args, **kwargs)
        # No se puede agregar items de otras lineas bases que esten es estado abierta o cerrada
        items_aprobados_queryset = Item.objects.filter(fase=id_fase).filter(Q(estado='Aprobado') & Q(last_release=True))
        lb_fase_queryset = LineaBase.objects.filter(fase=id_fase)
        for lb in lb_fase_queryset:
            if lb.estado == 'Abierta' or lb.estado == 'Cerrada':
                for item in lb.items.all():
                    if items_aprobados_queryset.filter(id=item.id).exists() and not kwargs['instance'].items.filter(
                            id=item.id).exists():
                        items_aprobados_queryset = items_aprobados_queryset.exclude(id=item.id)
        self.fields['items'].queryset = items_aprobados_queryset

    class Meta:
        model = LineaBase
        fields = [
            'items'
        ]

        labels = {
            'items': 'Items aprobados de la fase'
        }

        widgets = {
            'items': forms.CheckboxSelectMultiple()
        }

# **Volver atras** : [[apps.py]]

# **Ir a la documentación del modelo linea base** : [[models.py]]

# === Indice de la documentación de la Aplicación linea base  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)