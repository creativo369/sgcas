# === Importamos las librerias necesarias para la implementación de un Formulario ===
from django import forms

from apps.fase.models import Fase
from apps.item.models import Item
from apps.tipo_item.models import TipoItem


# === Clase para abstraer en un formulario el registro de un item ===
class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia de una fase la cual se desea crear
        un item.<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo fase<br/>
        """
        id_fase = kwargs.pop('id_fase')
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['estado'].disabled = True
        self.fields['usuarios_a_cargo'].queryset = Fase.objects.get(id=id_fase).miembros.all()

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
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Cantidad de horas estimativas, ejemplo: 7'}),
            'usuarios_a_cargo': forms.CheckboxSelectMultiple(),
            'archivo': forms.FileInput()
        }


# === Clase para abstraer en un formulario de importación de tipo_de_item ===
class ItemImportarTipoItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia de la fase la cual se desea crear
        un item.<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo fase<br/>
        """
        super(ItemImportarTipoItemForm, self).__init__(*args, **kwargs)
        fields_not_required = ('nombre', 'descripcion', 'estado', 'costo', 'usuarios_a_cargo')
        if 'instance' in kwargs:
            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True
            tipo_item_default = TipoItem.objects.first()
            self.fields['tipo_item'].initial = tipo_item_default

    # **Clase Meta para para el despliegue en una plantilla de los campos necesarios del modelo**
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


# === Clase para abstraer en un formulario de atributos de un item ===
class ItemAtributosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemAtributosForm, self).__init__(*args, **kwargs)
        """
        Constructor que se encarga de filtrar solo los atributos disponibles para un item<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo item<br/>
        """
        fields_not_required = ('nombre', 'descripcion', 'estado', 'costo', 'usuarios_a_cargo', 'tipo_item')

        # No se hacen seleccionables los atributos que no le corresponden al item segun su tipo de item
        if 'instance' in kwargs:
            attr_list = str(kwargs['instance'].tipo_item.atributos).split(',')

            # La lista de atributos se pasan a minuscula y se borran todos los espacios
            for i in range(len(attr_list)):
                attr_list[i] = (attr_list[i].lower()).strip()

            if 'boolean' not in attr_list:
                self.fields['boolean'].required = False
                self.fields['boolean'].disabled = True

            if 'char' not in attr_list:
                self.fields['char'].required = False
                self.fields['char'].disabled = True

            if 'date' not in attr_list:
                self.fields['date'].required = False
                self.fields['date'].disabled = True

            if 'numerico' not in attr_list:
                self.fields['numerico'].required = False
                self.fields['numerico'].disabled = True

            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True

    # **Clase Meta para para el despliegue en una plantilla de los campos necesarios del modelo**
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


# === Clase para abstraer en un formulario la modificación de un item ===
class ItemUpdateForm(forms.ModelForm):

    # Para read-only los fields nombre y estado
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los campos disponibles para cambiar los estados un item<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo item<br/>
        """
        id_fase = kwargs.pop('id_fase')
        super(ItemUpdateForm, self).__init__(*args, **kwargs)
        self.fields['usuarios_a_cargo'].queryset = Fase.objects.get(id=id_fase).miembros.all()
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


# === Clase para abstraer en un formulario el cambio de estado de un item===
class ItemCambiarEstado(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los campos disponibles para cambiar los estados un item<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo item<br/>
        """
        fields_not_required = ('nombre', 'descripcion', 'costo', 'usuarios_a_cargo')
        super(ItemCambiarEstado, self).__init__(*args, **kwargs)
        if kwargs['instance'].estado == 'Desarrollo':
            item_estado = [
                ('Desarrollo', 'Desarrollo'),
                ('Aprobado', 'Aprobado'),
                ('Desactivado', 'Desactivado'),
            ]
            self.fields['estado'].choices = item_estado
        if kwargs['instance'].estado == 'Revision':
            item_estado = [
                ('Revision', 'Revision'),
                ('Aprobado', 'Aprobado'),
                ('Desactivado', 'Desactivado'),
            ]
            self.fields['estado'].choices = item_estado
        if kwargs['instance'].estado == 'Aprobado':
            item_estado = [
                ('Aprobado', 'Aprobado'),
                ('Desactivado', 'Desactivado'),
            ]
            self.fields['estado'].choices = item_estado
        for field in fields_not_required:
            self.fields[field].required = False
            self.fields[field].disabled = True

    class Meta(ItemForm.Meta):
        model = Item


class RelacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('query')
        flag = kwargs.pop('flag')
        super(RelacionForm, self).__init__(*args, **kwargs)
        if flag == 0:
            fields_not_required = ('antecesores', 'sucesores')
            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True
            self.fields['hijos'].queryset = queryset
        elif flag == -1:
            fields_not_required = ('hijos', 'sucesores')
            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True
            self.fields['antecesores'].queryset = queryset
        else:
            fields_not_required = ('antecesores', 'hijos')
            for field in fields_not_required:
                self.fields[field].required = False
                self.fields[field].disabled = True
            self.fields['sucesores'].queryset = queryset

    class Meta:
        model = Item

        fields = [
            'hijos',
            'antecesores',
            'sucesores',
        ]

        labels = {
            'hijos': 'Hijos',
            'antecesores': 'Antecesores',
            'sucesores': 'Sucesores',
        }

        widgets = {
            'hijos': forms.CheckboxSelectMultiple(),
            'antecesores': forms.CheckboxSelectMultiple(),
            'sucesores': forms.CheckboxSelectMultiple(),
        }

# **Volver atras** : [[apps.py]]

# **Ir a la documentación del modelo comité** : [[models.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
