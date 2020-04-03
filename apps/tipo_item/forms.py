from django import forms
from apps.tipo_item.models import TipoItem

class TipoItemForm(forms.ModelForm):

	class Meta:
		model = TipoItem

		fields = [
			'nombre',
			'descripcion',
		]

		labels = {
			'nombre': 'Nombre',
			'descripcion': 'Descripcion',
		}

		widgets = {
			'nombre': forms.TextInput(attrs = {'class': 'form-control'}),
			'descripcion': forms.TextInput(attrs = {'class': 'form-control'}),
		}