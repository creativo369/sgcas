from django.contrib.auth.models import Group, Permission
from django import forms
from django.db.models import Q

# ** Clase que despliega el formulario de registro de un rol **
from apps import fase
from apps.fase.models import Fase
from apps.rol.models import Rol
from apps.usuario.models import User


# === ROLES POR FASES ===
class GroupForm(forms.ModelForm):
    # ** Despliega un filtro de los permisos en el sistema **
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(codename='editar_fase')
        | Q(codename='detalles_fase')
        | Q(codename='eliminar_fase')
        | Q(codename='cambio_estado_fase')
        | Q(codename='crear_item')
        | Q(codename='editar_item')
        | Q(codename='listar_item')
        | Q(codename='ver_item')
        | Q(codename='eliminar_item')
        | Q(codename='cambiar_estado_item')
        | Q(codename='relacion_item')
        | Q(codename='calcular_impacto')
        | Q(codename='ver_trazabilidad')
        | Q(codename='versiones_item')
        | Q(codename='restaurar_item_version')
        | Q(codename='item_modificar_atributos')
        | Q(codename='item_modificar_ti')
        | Q(codename='item_modificar_atributos_ti')
        | Q(codename='item_modificar_import_ti')
        | Q(codename='crear_tipo_item')
        | Q(codename='editar_tipo_item')
        | Q(codename='listar_tipo_item')
        | Q(codename='ver_tipo_item')
        | Q(codename='eliminar_tipo_item')
        | Q(codename='adjuntar_tipo_item')
        | Q(codename='importar_tipo_item')
        | Q(codename='crear_linea_base')
        | Q(codename='editar_linea_base')
        | Q(codename='eliminar_linea_base')
        | Q(codename='listar_linea_base')
        | Q(codename='estado_linea_base')
        | Q(codename='agregar_item_linea_base')
        | Q(codename='quitar_item_linea_base')
        | Q(codename='listar_item_linea_base')
        | Q(codename='crear_rol')
        | Q(codename='editar_rol')
        | Q(codename='listar_rol')
        | Q(codename='eliminar_rol')
        | Q(codename='asignar_rol')
    ),
        required=False,
        # widget=forms.Select(attrs={'class':'form-control'}))
    )

    # los campos del formulario
    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]

    labels = {  # etiquetas para el campo.
        'name': 'Nombre del rol',
        'permissions': 'Permisos',
    }


class RolFormUser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Constructor que se encarga de filtrar solo los miembros de la instancia de un proyecto para la fase a la cual se desea crear
        una fase.<br/>
        *:param args:**<br/>
        **:param kwargs:** diccionario de la referencia (_id) de la instancia del modelo proyecto<br/>
        """
        super(RolFormUser, self).__init__(*args, **kwargs)
        rol = kwargs['instance'].fase.miembros.all()
        self.fields['usuarios'].queryset = rol

    class Meta:
        model = Rol

        fields = [  # campos de mi modelo
            'usuarios',
        ]
        labels = {
            'usuarios': 'Miembros de la fase'
        }
        # los aparatos o elementos de captura de información del formulario
        widgets = {
            'usuarios': forms.CheckboxSelectMultiple(),
        }


# === ROL SISTEMA ===
class GroupForm_sistema(forms.ModelForm):
    # ** Despliega un filtro de los permisos en el sistema **
    # permiso = Permission.objects.get(codename='crear_proyecto')
    # print(permiso.name)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(codename='crear_rol_sistema')
        | Q(codename='editar_rol_sistema')
        | Q(codename='gestion_rol_sistema')
        | Q(codename='listar_rol_sistema')
        | Q(codename='eliminar_rol_sistema')
        | Q(codename='asignar_rol_sistema')
        | Q(codename='registrar_usuario')
        | Q(codename='editar_usuario')
        | Q(codename='eliminar_usuario')
        | Q(codename='ver_usuario')
        | Q(codename='gestion_usuario')
        | Q(codename='ver_mensaje')
        | Q(codename='mensaje_editar')
        | Q(codename='mensaje_rechazar')
        | Q(codename='crear_proyecto')
        | Q(codename='editar_proyecto')
        | Q(codename='ver_proyecto')
        | Q(codename='gestion_proyecto')
        | Q(codename='eliminar_proyecto')
        | Q(codename='cambiar_estado')
        | Q(codename='detalles_proyecto')
        | Q(codename='crear_comite')
        | Q(codename='editar_comite')
        | Q(codename='ver_comite')
        | Q(codename='eliminar_comite')
        | Q(codename='crear_fase')
        | Q(codename='listar_fase')
        | Q(codename='gestion_fase')
        # === Permisos para roles por fase
        # | Q(codename='crear_rol')
        # | Q(codename='editar_rol')
        # | Q(codename='listar_rol')
        # | Q(codename='eliminar_rol')
        # | Q(codename='asignar_rol')
    ),
        required=True,
        # widget=forms.Select(attrs={'class':'form-control'}))
    )

    # los campos del formulario
    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]

    labels = {  # etiquetas para el campo.
        'name': 'Nombre del rol',
        'permissions': 'Permisos',
    }

# === FIN ===
# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
