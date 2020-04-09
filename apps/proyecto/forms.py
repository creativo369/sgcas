from django import forms
from .models import Proyecto
from django.contrib.auth.models import User


class ProjectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto

        fields = [  # campos de mi modelo
            'nombre',
            'descripcion',
            'miembros',
        ]
        labels = {  # las etiquetas que tendra para visualizarse en el navegador
            'nombre': 'Nombre del Proyecto',
            'descripcion': 'Descripción del Proyecto',
            'miembros': 'Miembros',
        }
        widgets = {  # los aparatos o elementos de captura de información del formulario
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea,
            'miembros': forms.CheckboxSelectMultiple()
        }
        #
        # problems = forms.ModelMultipleChoiceField(
        #     widget=forms.CheckboxSelectMultiple,
        #     queryset=Problem.objects.all()
        # )
