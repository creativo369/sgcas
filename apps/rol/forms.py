from django.contrib.auth.models import Group, Permission
from django import forms
from django.db.models import Q


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        Q(codename__icontains='logentry')
        | Q(name='Can add proyecto')
        | Q(name='Can change proyecto')
        | Q(name='Can delete proyecto')
        | Q(name='Can view proyecto')
        | Q(name='Can add comite')
        | Q(name='Can change comite')
        | Q(name='Can delete comite')
        | Q(name='Can view comite')
        | Q(name='Can add item')
        | Q(name='Can change item')
        | Q(name='Can delete item')
        | Q(name='Can view item')
        | Q(name='Can add user')
        | Q(name='Can change user')
        | Q(name='Can delete user')
        | Q(name='Can view user')
    ))

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]

    labels = {
        'name': 'Nombre del rol',
        'permissions': 'Permisos',
    }
