from django.contrib.auth.models import Group
from django import forms

class GroupForm(forms.ModelForm):
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