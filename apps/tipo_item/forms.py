from django import forms
from apps.tipo_item.models import TipoItem, ATTRIBUTES

class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem

        atributos = forms.MultipleChoiceField(choices=ATTRIBUTES)

        fields = [
            'nombre',
            'descripcion',
            'atributos',
        ]

        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'atributos': 'Atributos',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca un nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una breve descripción', 'rows': 4,
                                                 'cols': 15}),
            'atributos': forms.CheckboxSelectMultiple()
        }


class TipoItemUpdateForm(TipoItemForm):

    #Field nombre read-only en update
    def __init__(self, *args, **kwargs):
        super(TipoItemUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['nombre'].required = False
            self.fields['nombre'].disabled = True


    class Meta(TipoItemForm.Meta):
        model = TipoItem