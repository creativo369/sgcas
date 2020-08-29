from django.contrib.auth.models import Group, Permission
from django import forms
from django.db.models import Q


# ** Clase que despliega el formulario de registro de un rol **
class GroupForm(forms.ModelForm):
    # ** Despliega un filtro de los permisos en el sistema **

    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(name='crear_linea_base')
        | Q(name='cerrar_linea_base')
        | Q(name='ver_linea_base')
        | Q(name='editar_linea_base')
        | Q(name='agregar_item_linea_base')
        | Q(name='listar_item_linea_base')
        | Q(name='quitar_item_linea_base')
        | Q(name='estado_linea_base')
        | Q(name='crear_rol')
        | Q(name='eliminar_rol')
        | Q(name='asignar_rol')
        | Q(name='ver_rol')
        | Q(name='ver_usuarios')
        | Q(name='listar_rol')
        | Q(name='editar_rol')
        | Q(name='agregar_usuario_fase')
        | Q(name='quitar_usuario_fase')
        | Q(name='crear_fase')
        | Q(name='aprobar_fase')
        | Q(name='editar_fase')
        | Q(name='eliminar_fase')
        | Q(name='crear_fase')
        | Q(name='ver_fase')
        | Q(name='listar_fase')
        | Q(name='cambio_estado_fase')
        | Q(name='detalles_fase')
        | Q(name='crear_item')
        | Q(name='aprobar_item')
        | Q(name='ver_trazabilidad')
        | Q(name='editar_item')
        | Q(name='item_modificar_atributos')
        | Q(name='item_modificar_atributos_ti')
        | Q(name='item_modificar_import_ti')
        | Q(name='cambiar_estado_item')
        | Q(name='listar_item_de_fase')
        | Q(name='eliminar_item')
        | Q(name='relacionar_item')
        | Q(name='restaurar_item_version')
        | Q(name='ver_item')
        | Q(name='ver_versiones_item')
        | Q(name='crear_tipo_item')
        | Q(name='adjuntar_tipo_item')
        | Q(name='editar_tipo_item')
        | Q(name='item_modificar_ti')
        | Q(name='eliminar_tipo_item')
        | Q(name='importar_tipo_item')
        | Q(name='ver_tipo_item')
        | Q(name='listar_tipo_item')
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


# === ROL SISTEMA ===
class GroupForm_sistema(forms.ModelForm):
    # ** Despliega un filtro de los permisos en el sistema **

    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(name='crear_proyecto')
        | Q(name='iniciar_proyecto')
        | Q(name='finalizar_proyecto')
        | Q(name='cancelar_proyecto')
        | Q(name='ver_proyecto')
        | Q(name='detalles_proyecto')
        | Q(name='editar_proyecto')
        | Q(name='eliminar_proyecto')
        | Q(name='crear_usuario')
        | Q(name='editar_usuario')
        | Q(name='agregrar_usuario_proyecto')
        | Q(name='eliminar_usuario')
        | Q(name='mensaje_eliminar')
        | Q(name='ver_mensaje')
        | Q(name='mensaje_editar')
        | Q(name='crear_rol_sistema')
        | Q(name='eliminar_rol_sistema')
        | Q(name='asignar_rol_sistema')
        | Q(name='ver_rol_sistema')
        | Q(name='ver_usuarios')
        | Q(name='listar_rol_sistema')
        | Q(name='editar_rol_sistema')
        | Q(name='agregar_usuario_fase')
        | Q(name='crear_fase')
        | Q(name='ver_fase')
        | Q(name='listar_fase')
        | Q(name='detalles_fase')
        | Q(name='quitar_usuario_proyecto')
        | Q(name='quitar_usuario_fase')
        | Q(name='crear_comite')
        | Q(name='eliminar_comite')
        | Q(name='ver_comite')
        | Q(name='editar_comite')
        | Q(name='listar_comite')
        | Q(name='agregar_comite_proyecto')
        | Q(name='"quitar_comite_proyecto"')
        | Q(name='agregar_usuario_comite')
        | Q(name='quitar_usuario_comite')
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
