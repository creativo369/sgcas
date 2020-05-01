from django import forms
from .models import Proyecto


class FormularioProyecto(forms.ModelForm):
    """
    Clase que modela el formulario de la definición de un proyecto a ser usado en la plantilla
    """

    # Para read - only los fields estado y fecha_creacion

    def __init__(self, *args, **kwargs):
        super(FormularioProyecto, self).__init__(*args, **kwargs)
        campos = ['fecha_creacion', 'estado']
        for field in campos:
            self.fields[field].required = False
            self.fields[field].disabled = True

    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
            'miembros',
            'fecha_creacion',
            'estado',

        ]
        # Las etiquetas que tendrá para visualizarse en el navegador
        labels = {
            'nombre': 'Nombre del Proyecto',
            'descripcion': 'Descripción del Proyecto',
            'miembros': 'Miembros',
            'fecha_creacion': 'Fecha de Creación',
            'estado': 'Estado actual',
        }
        # los aparatos o elementos de captura de información del formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca el nombre del proyecto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una descripción al proyecto'}),
            'miembros': forms.CheckboxSelectMultiple(),
            'fecha_creacion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormularioProyectoUpdate(FormularioProyecto):
    """
    Clase que modela el formulario de la definición de un proyecto a ser usado en la plantilla
    """

    # Para read - only los fields que se presentan en la siguiente lista.

    def __init__(self, *args, **kwargs):
        super(FormularioProyectoUpdate, self).__init__(*args, **kwargs)

        # fields representa los campos que no son editables de acuerdo al estado del proyecto
        fields = ['nombre', 'fecha_creacion', 'estado']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre del proyecto si su estado es pendiente
           # if kwargs['instance'].estado == 'Pendiente' or kwargs['instance'].estado == 'Iniciado' or \
               #     kwargs['instance'].estado == 'Finalizado' or kwargs['instance'].estado == 'Cancelado':
                for field in fields:
                    self.fields[field].required = False
                    self.fields[field].disabled = True

    class Meta(FormularioProyecto.Meta):
        model = Proyecto


class ChangeProject(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChangeProject, self).__init__(*args, **kwargs)
        # fields representa los campos que no son editables de acuerdo al estado del proyecto
        fields = ['nombre', 'descripcion', 'fecha_creacion', 'miembros']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre del proyecto si su estado es pendiente
            # if kwargs['instance'].estado == 'Pendiente':
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
            'miembros',
            'fecha_creacion',
            'estado',

        ]
        labels = {
            'estado': 'Cambiar de estado',
        }
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
