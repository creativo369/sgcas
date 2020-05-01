from django import forms
from .models import Comite
from ..proyecto.models import Proyecto


class FormularioComite(forms.ModelForm):
    """
        Formulario para el registro de comité
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia del proyecto la cual se desea crear
        un comité de aprovación.
        :param args:
        :param kwargs: diccionario de la referencia (_id) de la instancia del modelo proyecto
        """
        _id = kwargs.pop('_id')  # Se obtiene el id del proyecto a traves del kwargs
        super(FormularioComite, self).__init__(*args, **kwargs)  # Se inicializa el formulario
        self.fields['miembros'].queryset = Proyecto.objects.get(
            id=_id).miembros.all()  # Se filtra el queryset para miembros

    class Meta:
        model = Comite
        """
            Campos requeridos para la definición de un comité 
        """
        fields = [
            'nombre',
            'descripcion',
            'miembros',
        ]
        """
            Etiquetas para el campo
        """
        labels = {
            'nombre': 'Asigne un nombre al comite del Proyecto',
            'descripcion': 'Descripción breve de responsabilidades de la comisión',
        }
        """
            Para obtener los datos y almacenar en la base de datos
        """
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'miembros': forms.CheckboxSelectMultiple(),
        }


class FormularioComiteUpdate(forms.ModelForm):
    class Meta(FormularioComite.Meta):
        model = Comite
