# === Importamos las librerias necesarias para la implementación de un Formulario ===
from django import forms
from .models import Comite, Solicitud
from ..proyecto.models import Proyecto
from ..linea_base.models import LineaBase
from ..item.models import Item
from django.shortcuts import get_object_or_404
from apps.item.views import get_lb


# === Clase para abstraer en un formulario el registro de un Comité ===
class FormularioComite(forms.ModelForm):
    # ** Formulario para el registro de comité **
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia del proyecto la cual se desea crear
        un comité de aprobación.<br/>
        **:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo proyecto<br/>
        """
        _id = kwargs.pop('_id')  # Se obtiene el id del proyecto a traves del kwargs
        super(FormularioComite, self).__init__(*args, **kwargs)  # Se inicializa el formulario
        self.fields['miembros'].queryset = Proyecto.objects.get(
            id=_id).miembros.all()  # Se filtra el queryset para miembros

    # **Clase Meta para para el despliegue en una plantilla de los campos necesarios del modelo**
    class Meta:
        model = Comite
        # **Campos requeridos para la definición de un comité**
        fields = [
            'nombre',
            'descripcion',
            'miembros',
        ]
        # **Etiquetas para el campo**
        labels = {
            'nombre': 'Asigne un nombre al comite del Proyecto',
            'descripcion': 'Descripción breve de responsabilidades de la comisión',
        }
        # **Aparatos para formatear un formulario con el respectivo campo**
        # Para obtener los datos y almacenar en la base de datos
        widgets = {

            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Asigne un nombre al comité'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control',
                                            'placeholder': 'Agregue una breve descripción'}),

            'miembros': forms.CheckboxSelectMultiple(),
        }


# === Clase heredada para abstraer en un formulario la actualización de un Comité ===
class FormularioComiteUpdate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormularioComiteUpdate, self).__init__(*args, **kwargs)
        self.fields['miembros'].queryset = kwargs['instance'].proyecto.miembros.all()

    class Meta(FormularioComite.Meta):
        model = Comite


class FormularioSolicitud(forms.ModelForm):
    def __init__(self, *args, **kwargs):             
        
        request = kwargs.pop('request') 
        pk = kwargs.pop('pk')      

        super(FormularioSolicitud, self).__init__(*args, **kwargs)
        fields_not_required = ['asunto', 'solicitante', 'item', 'tipo', 'linea_base', 'votacion','en_proceso','realizacion']
        
        self.fields['solicitante'].initial = request.user
        self.fields['proyecto'].initial = Item.objects.get(pk=pk).fase.proyecto
        

        for field in fields_not_required:
            self.fields[field].required = False
            self.fields[field].disabled = True

        
        self.fields['asunto'].initial = 'Item: {} | Fase: {} | Proyecto: {}.'.format( Item.objects.get(pk=pk),Item.objects.get(pk=pk).fase, Item.objects.get(pk=pk).fase.proyecto)
        self.fields['item'].initial = Item.objects.get(pk=pk)
        self.fields['linea_base'].initial = None

    class Meta:
        model = Solicitud
        fields = '__all__'
        labels = {'asunto':'Asunto', 'Descripción':'descripcion'}
        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Ingrese una descripción para la solicitud.'}),
        }


# **Volver atras** : [[apps.py]]

# **Ir a la documentación del modelo comité** : [[models.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)