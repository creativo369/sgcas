# === Importamos las librerias necesarias para la implementación de un Formulario ===
from django import forms
from .models import Fase, Proyecto

# === Clase para abstraer en un formulario el registro de una fase ===
from ..item.models import Item
from ..linea_base.models import LineaBase


# ** Formulario para el registro de una fase **
class FaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia de un proyecto para la fase a la cual se desea crear
        una fase.<br/>
        *:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo proyecto<br/>
        """
        _id = kwargs.pop('_id')
        super(FaseForm, self).__init__(*args, **kwargs)
        self.fields['miembros'].queryset = Proyecto.objects.get(id=_id).miembros.all()
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True

    # **Clase Meta para para el despliegue en una plantilla de los campos necesarios del modelo**
    class Meta:
        model = Fase
        # **Campos requeridos para la definición de una fase**
        fields = [  # campos de mi modelo
            'nombre',
            'descripcion',
            'estado',
            'miembros',
        ]
        # las etiquetas que tendra para visualizarse en el navegador
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'miembros': 'Miembros',
        }
        # los aparatos o elementos de captura de información del formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca el nombre de la nueva fase'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una breve descripcion de la fase',
                                                 'rows': 5,
                                                 'cols': 50}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'miembros': forms.CheckboxSelectMultiple()

        }


# === Clase heredada para abstraer en un formulario la actualización de una fase ===
class FaseUpdateForm(forms.ModelForm):
    # Para read-only los fields nombre y estado
    def __init__(self, *args, **kwargs):
        """
        Constructor de la clase para obtener el diccionario de los datos de la instancia del formulario de una fase<br/>
        **:param args:** <br/>
        **:param kwargs:** recibe el diccionario con los datos de la fase <br/>
        """
        super(FaseUpdateForm, self).__init__(*args, **kwargs)
        # fields representa los campos que no son editables de acuerdo al estado de la fase
        fields = ['estado']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre de la fase si su estado no es Abierta
            if kwargs['instance'].estado == 'Abierta':
                fields.append('nombre')
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(FaseForm.Meta):
        model = Fase


# ** Clase que se utiliza para el cambio de estado de una fase **
class FaseCambiarEstadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Recibimos los datos a traves de un formulario y restringimos los cambios que no se pueden modificar solamente
        son para lectura.<br/>
        **:param args:**<br/>
        **:param kwargs:** el diccionario que contiene los datos de una instancia del modelo de una fase<br/>
        """
        fields_not_required = ('nombre', 'descripcion', 'miembros')
        super(FaseCambiarEstadoForm, self).__init__(*args, **kwargs)
        for field in fields_not_required:
            self.fields[field].required = False
            self.fields[field].disabled = True

        # Para cerrar una fase todas las lineas bases deben de estar cerradas
        # No debe de haber un solo item sin linea base
        total_items_fase = Item.objects.filter(fase=kwargs['instance'].id).count()
        lb_fase_queryset = LineaBase.objects.filter(fase=kwargs['instance'].id)
        items_en_lb = 0
        fase_estado_opciones = [('Abierta', 'Abierta'), ('Cerrada', 'Cerrada')]
        print(fase_estado_opciones)
        for lb in lb_fase_queryset:
            items_en_lb += lb.items.all().count()
            if lb.estado == 'Abierta':
                fase_estado_opciones = [('Abierta', 'Abierta')]
                break
        if total_items_fase - items_en_lb != 0:
            fase_estado_opciones = [('Abierta', 'Abierta')]
        self.fields['estado'].choices = fase_estado_opciones

    class Meta(FaseForm.Meta):
        model = Fase
# **Volver atras** : [[apps.py]]

# **Ir a la documentación del modelo comité** : [[models.py]]

# === Indice de la documentación de la Aplicación fase  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
