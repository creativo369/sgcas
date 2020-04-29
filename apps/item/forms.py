from django import forms
from apps.item.models import Item
from apps.tipo_item.models import TipoItem


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True

    class Meta:
        model = Item

        fields = [  # campos de mi modelo
            'nombre',
            'descripcion',
            'estado',
            'costo',
            'usuarios_a_cargo',
            'archivo'
        ]
        labels = {  # las etiquetas que tendra para visualizarse en el navegador
            'nombre': 'Nombre del Item',
            'descripcion': 'Descripción del Item',
            'estado': 'Estado',
            'costo': 'Costo',
            'usuarios_a_cargo': 'Usuarios a cargo',
            'archivo': 'Archivo'
        }
        widgets = {  # los aparatos o elementos de captura de información del formulario
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Introduzca un nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Agregue una breve descripción', 'rows': 4,
                                                 'cols': 15}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Cantidad de horas estimativas, ejemplo: 7'}),
            'usuarios_a_cargo': forms.CheckboxSelectMultiple(),
            'archivo': forms.FileInput()
        }


class ItemImportarTipoItemForm(ItemForm):

    def __init__(self, *args, **kwargs):
        super(ItemImportarTipoItemForm, self).__init__(*args, **kwargs)
        fields_not_required = ('nombre', 'descripcion', 'estado', 'costo', 'usuarios_a_cargo')
        if 'instance' in kwargs:
            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True
            tipo_item_default = TipoItem.objects.first()
            self.fields['tipo_item'].initial = tipo_item_default

    class Meta(ItemForm.Meta):
        model = Item

        fields = [
            'nombre',
            'descripcion',
            'estado',
            'costo',
            'usuarios_a_cargo',
            'tipo_item',
        ]
        labels = {
            'tipo_item': 'Importar tipo de item',
        }
        widgets = {
            'tipo_item': forms.RadioSelect(),
        }


class ItemAtributosForm(ItemForm):

    def __init__(self, *args, **kwargs):
        super(ItemAtributosForm, self).__init__(*args, **kwargs)
        fields_not_required = ('nombre', 'descripcion', 'estado', 'costo', 'usuarios_a_cargo', 'tipo_item')

        # No se hacen seleccionables los atributos que no le corresponden al item segun su tipo de item
        if 'instance' in kwargs:
            attr_list = str(kwargs['instance'].tipo_item.atributos).split(',')

            # La lista de atributos se pasan a minuscula y se borran todos los espacios
            for i in range(len(attr_list)):
                attr_list[i] = (attr_list[i].lower()).strip()

            print(attr_list)

            if 'boolean' not in attr_list:
                print('Boolean esta')
                self.fields['boolean'].required = False
                self.fields['boolean'].disabled = True

            if 'char' not in attr_list:
                self.fields['char'].required = False
                self.fields['char'].disabled = True

            if 'date' not in attr_list:
                print('hola mundo')
                self.fields['date'].required = False
                self.fields['date'].disabled = True

            if 'numerico' not in attr_list:
                self.fields['numerico'].required = False
                self.fields['numerico'].disabled = True

            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(ItemForm.Meta):
        model = Item

        fields = [
            'nombre',
            'descripcion',
            'estado',
            'costo',
            'usuarios_a_cargo',
            'tipo_item',
            'boolean',
            'char',
            'date',
            'numerico',
        ]
        labels = {
            'bolean': 'Boolean',
            'char': 'Char',
            'date': 'Date',
            'numerico': 'Numerico',
        }
        widgets = {
            'bolean': forms.BooleanField(),
            'char': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduzca el atributo char'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'numerico': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Introduzca atributo numerico'}),
        }


class ItemUpdateForm(ItemForm):

    # Para read-only los fields nombre y estado
    def __init__(self, *args, **kwargs):
        super(ItemUpdateForm, self).__init__(*args, **kwargs)
        # fields representa los campos que no son editables de acuerdo al estado del item
        fields = ['estado']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre del item si su estado no es desarrollo
            if kwargs['instance'].estado == 'Desarrollo':
                fields.append('nombre')
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(ItemForm.Meta):
        model = Item
