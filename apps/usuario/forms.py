from django import forms
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings

##Mientras tanto no se admiten password
inactivo_previo = False

class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    roles = forms.ModelChoiceField(queryset=Group.objects.all())

    # widget=forms.CheckboxSelectMultiple como argumento para aceptar checkbox multiples.
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'email', 'username',
            'roles', 'is_active'
        ]

        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'username': 'Usuario',
            'roles': 'Roles',
            'is_active': 'Cuenta activa'
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
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

    def save(self):
        # password = self.cleaned_data.pop('password')
        roles = self.cleaned_data.pop('roles')
        u = super().save()
        u.groups.set([roles])
        # u.set_password(password)
        u.save()

        if u.is_active and inactivo_previo:
            subject = 'Registro SGCAS'
            message = 'Su cuenta ha sido aprobada satisfactoriamente, ya puede ingresar al sistema SGCAS'
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [u.email, settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        return u
