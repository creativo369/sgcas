from django import forms
from .models import Proyecto


class FormularioProyecto(forms.ModelForm):
    """
    Clase que modela el formulario de la definición de un proyecto a ser usado en la plantilla
    """

    # Para read - only los fields nombre y estado

    def __init__(self, *args, **kwargs):
        super(FormularioProyecto, self).__init__(*args, **kwargs)
        campos = ['estado', 'fecha_creacion']
        for field in campos:
            self.fields[field].required = False
            self.fields[field].disabled = True

    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
            'miembros',
            'estado',
            'fecha_creacion',
        ]
        # Las etiquetas que tendrá para visualizarse en el navegador
        labels = {
            'nombre': 'Nombre del Proyecto',
            'descripcion': 'Descripción del Proyecto',
            'miembros': 'Miembros',
            'estado': 'Estado actual',
            'fecha_creacion': 'Fecha de Creación',
        }
        # los aparatos o elementos de captura de información del formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca el nombre del proyecto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una descripción al proyecto'}),
            'miembros': forms.CheckboxSelectMultiple(),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_creacion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormularioProyectoUpdate(FormularioProyecto):
    """
    Clase que modela el formulario de la definición de un proyecto a ser usado en la plantilla
    """

    # Para read - only los fields que se presentan en la siguiente lista.

    def __init__(self, *args, **kwargs):
        super(FormularioProyectoUpdate, self).__init__(*args, **kwargs)

        # fields representa los campos que no son editables de acuerdo al estado del proyecto
        fields = ['nombre', 'estado', 'fecha_creacion']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre del proyecto si su estado es pendiente
            if kwargs['instance'].estado == 'Pendiente':
                for field in fields:
                    self.fields[field].required = False
                    self.fields[field].disabled = True

    class Meta(FormularioProyecto.Meta):
        model = Proyecto
