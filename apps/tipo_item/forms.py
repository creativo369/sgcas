from django import forms
from apps.tipo_item.models import TipoItem, ATTRIBUTES


# === Clase para abstraer en un formulario el registro de un Tipo de item ===
class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem
        # Elegimos los atributos que tendra el tipo de item
        atributos = forms.MultipleChoiceField(choices=ATTRIBUTES)
        # atributos del modelo
        fields = [
            'nombre',
            'descripcion',
            'atributos',
        ]
        # las etiquetas del formulario a ser desplegado en la plantilla
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'atributos': 'Atributos',
        }
        # elementos para el formulario del tipo de item
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca un nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una breve descripción', 'rows': 4,
                                                 'cols': 15}),
            'atributos': forms.CheckboxSelectMultiple()
        }

# === Clase para abstraer en un formulario para la actualización de un Tipo de item ===
class TipoItemUpdateForm(TipoItemForm):

    # Campo nombre read-only en update
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los campos que pueden ser modificados<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo tipo_de_item<br/>
                """
        super(TipoItemUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['nombre'].required = False
            self.fields['nombre'].disabled = True

    class Meta(TipoItemForm.Meta):
        model = TipoItem

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)