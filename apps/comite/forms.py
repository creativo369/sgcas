from django import forms
from .models import Comite


class FormularioComite(forms.ModelForm):
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
            'miembros': 'Asignar miembros',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'miembros': forms.CheckboxSelectMultiple(),
        }
