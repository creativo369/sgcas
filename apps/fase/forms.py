from django import forms
from .models import Fase, Proyecto
from django.contrib.auth.models import User

from ..item.models import Item
from ..linea_base.models import LineaBase


class FaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        _id = kwargs.pop('_id')
        super(FaseForm, self).__init__(*args, **kwargs)
        self.fields['miembros'].queryset = Proyecto.objects.get(id=_id).miembros.all()
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True

    class Meta:
        model = Fase

        fields = [  # campos de mi modelo
            'nombre',
            'descripcion',
            'estado',
            'miembros',
        ]
        labels = {  # las etiquetas que tendra para visualizarse en el navegador
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'miembros': 'Miembros',
        }
        widgets = {  # los aparatos o elementos de captura de información del formulario
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca el nombre de la nueva fase'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una breve descripcion de la fase',
                                                 'rows': 5,
                                                 'cols': 50}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'miembros': forms.CheckboxSelectMultiple()

        }


class FaseUpdateForm(forms.ModelForm):
    # Para read-only los fields nombre y estado
    def __init__(self, *args, **kwargs):
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


class FaseCambiarEstadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
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
