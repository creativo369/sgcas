from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms

class FormularioRegistro(UserCreationForm):
	groups = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True,widget=forms.Select(attrs={'class':'form-control'}))
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'groups'
		]
		labels = {
			'username': 'Usuario',
			'first_name': 'Nombres',
			'last_name': 'Apellidos',
			'email': 'Correo electronico',
			'groups': 'Roles'
		}

	def save(self, commit = True):
		user = super(FormularioRegistro, self).save(commit = False)
		if commit:
			user.save()
		return user

		widgets= {
				'username': forms.TextInput(attrs={'class':'form-control'}),
				'first_name': forms.TextInput(attrs={'class':'form-control'}),
				'last_name': forms.TextInput(attrs={'class':'form-control'}),
				'email': forms.EmailField(attrs={'class':'form-control'}),
			}
