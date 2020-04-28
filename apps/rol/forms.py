from django.contrib.auth.models import Group, Permission
from django import forms
from django.db.models import Q


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(
        # Q(codename__icontains='logentry'),

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
