from django import forms
from django.contrib.auth.models import Group
from django.core.mail import send_mail
# from django.conf import settings
from SGCAS.settings import base

from apps.usuario.models import User

# Mientras tanto no se admiten password
inactivo_previo = False


class UserForm(forms.ModelForm):
    roles = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        # Campos del modelo Rol
        fields = [
            'first_name', 'last_name',
            'email', 'username',
            'roles', 'is_active'
        ]
        # etiquetas de los campos del formulario
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'username': 'Usuario',
            'roles': 'Roles',
            'is_active': 'Estado de la Cuenta'
        }
        widgets = {  # los aparatos o elementos de captura de información del formulario
            'first_name': forms.Textarea(attrs={'class': 'form-control',
                                                'placeholder': 'Introduzca los nombres',
                                                'rows': 1,
                                                'cols': 10}),
            'last_name': forms.Textarea(attrs={'class': 'form-control',
                                               'placeholder': 'Introduzca los apellidos',
                                               'rows': 1,
                                               'cols': 10}),
            'email': forms.Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Introduzca el correo',
                                           'rows': 1,
                                           'cols': 10}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            """
            Constructor que se encarga de filtrar solo los usuarios habilitados y activos en el sistema.<br/>
            **:param args:**<br/>
            **:param kwargs:** diccionario de la referencia (_id) de cada instancia del modelo usuario<br/>
            """
            # Se obtiene el argumento kword si existe, o se lo inicializa
            # como un diccionario si no existe
            initial = kwargs.setdefault('initial', {})
            # El widget para el ModelMultiplceChoiceField espera una lista
            # de primarykey para los datos seleccionados

            if not kwargs['instance'].is_active:
                global inactivo_previo
                inactivo_previo = True

            if kwargs['instance'].groups.all():
                initial['roles'] = kwargs['instance'].groups.all()[0]
            else:
                initial['roles'] = None

            forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Guarda el formulario .<br/>
        :return:
        """
        roles = self.cleaned_data.pop('roles')
        u = super().save()
        u.groups.set([roles])
        u.save()

        if u.is_active and inactivo_previo:
            subject = 'Registro SGCAS'

            message = 'Hola ' + u.username + '!. Su cuenta ha sido aprobada satisfactoriamente, ya puede ingresar al sistema SGCAS'

            send_mail(
                subject,
                message,
                base.EMAIL_HOST_USER,
                [u.email, base.EMAIL_HOST_USER],
                fail_silently=False,
            )
        return u



class FormularioUsuarioActivar(UserForm):
    # **Clase que modela el formulario de la definición de un usuario a ser usado en la plantilla**<br/>

    # Para read - only los fields que se presentan en la siguiente lista.<br/>
    def __init__(self, *args, **kwargs):
        super(FormularioUsuarioActivar, self).__init__(*args, **kwargs)

        # fields representa los campos que no son editables de acuerdo al estado del proyecto<br/>
        fields = ['first_name', 'last_name', 'email', 'username']
        if 'instance' in kwargs:
            # No se permite la modificacion del nombre ,apellidos , correo electronico , Usuario<br/>
            for field in fields:
                self.fields[field].required = False
                self.fields[field].disabled = True

    class Meta(UserForm.Meta):
        model = User

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>