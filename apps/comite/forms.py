from django import forms
from .models import Comite
from ..proyecto.models import Proyecto
from django.contrib.auth.models import User


class FormularioComite(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        _id = kwargs.pop('_id') ##Se obtiene el id del proyecto a traves del kwargs
        super(FormularioComite, self).__init__(*args, **kwargs) #Se inicializa el formulario
        self.fields['miembros'].queryset = Proyecto.objects.get(id=_id).miembros.all() ##Se filtra el queryset para miembros

    class Meta:
        model = Comite

        fields = [
            'nombre',
            'descripcion',
            'miembros',
        ]
        labels = {
            'nombre': 'Asigne un nombre al comite del Proyecto',
            'descripcion': 'Descripción breve de responsabilidades de la comisión',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'miembros': forms.CheckboxSelectMultiple(),
        }
