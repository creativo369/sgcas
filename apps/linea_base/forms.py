from django import forms
from .models import LineaBase
from django.contrib.auth.models import User

from ..fase.models import Fase
from ..item.models import Item


class LineaBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True

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


class LineaBaseUpdateEstado(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LineaBaseUpdateEstado, self).__init__(*args, **kwargs)

        self.fields['descripcion'].required = False
        self.fields['descripcion'].disabled = True

    class Meta(LineaBaseForm.Meta):
        model = LineaBase


class LineaBaseUpdateForm(LineaBaseForm):

    # Para read-only el field estado
    def __init__(self, *args, **kwargs):
        super(LineaBaseUpdateForm, self).__init__(*args, **kwargs)
        # fields representa los campos que no son editables de acuerdo al estado de la linea base
        fields = ['estado']
        if 'instance' in kwargs:
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(LineaBaseForm.Meta):
        model = LineaBase


class AgregarItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        super(AgregarItemsForm, self).__init__(*args, **kwargs)
        ##No se puede agregar items de otras lineas bases que esten es estado abierta o cerrada
        items_aprobados_queryset = Item.objects.filter(fase=id_fase).filter(estado='Aprobado')
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
