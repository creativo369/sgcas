from django.contrib.auth.models import Group, Permission
from django import forms
from django.db.models import Q


# ** Clase que despliega el formulario de registro de un rol **
class GroupForm(forms.ModelForm):
    # ** Despliega un filtro de los permisos en el sistema **
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(codename__icontains='logentry')
        | Q(name='Puede crear un proyecto')
        | Q(name='Puede editar el proyecto')
        | Q(name='Puede eliminar un proyecto')
        | Q(name='Puede visualizar un proyecto')
        | Q(name='Puede crear un comité')
        | Q(name='Puede editar el comité')
        | Q(name='Puede eliminar un comité')
        | Q(name='Puede visualizar un comité')
        | Q(name='Puede crear un item')
        | Q(name='Puede editar el item')
        | Q(name='Puede eliminar un item')
        | Q(name='Puede visualizar un item')
        | Q(name='Puede crear un usuario')
        | Q(name='Puede editar el usuario')
        | Q(name='Puede eliminar un usuario')
        | Q(name='Puede visualizar un usuario')
        | Q(name='Puede crear un tipo de item')
        | Q(name='Puede editar el tipo de item')
        | Q(name='Puede eliminar un tipo de item')
        | Q(name='Puede visualizar un tipo de item')
    ))

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

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>
