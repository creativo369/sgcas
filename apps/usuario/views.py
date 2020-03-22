from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView , UpdateView , DeleteView
from django.contrib.auth.models import User,Group
from apps.usuario.forms import FormularioRegistro
from django.urls import reverse_lazy

# Create your views here.
@login_required
def usuario_view(request):
    """
    Args:
    	Se recibe un request una vez validado el login
    Returns:
    	html: Retorna una pagina renderizada de bienvenida al usuario
    """
    return render(request, 'usuario/usuario_home.html')

def usuario_opciones(request):
   # """
   #  Args:
   #  	Se recibe un request una vez validado el login
   #  Returns:
   #  	html:Se renderiza una pagina con las opciones que se realiza sobre un usuario
   #  """
  return render(request, 'usuario/usuario_opciones.html')


class UsuarioLista(PermissionRequiredMixin, ListView):
	model = User
	template_name = 'usuario/usuario_lista.html'
	permission_required = 'auth.change_user'


class RegistrarUsuario(PermissionRequiredMixin, CreateView):

	model = User
	template_name = 'usuario/usuario_registrar.html'
	form_class = FormularioRegistro
	permission_required = 'auth.add_user'

	def for_valid(self, form):
		response = super(RegistrarUsuario, self).form_valid(form)
		username = form.cleaned_data['username']
		rol = form.cleaned_data['groups']
		g = Group.objects.get(name = rol)
		g.user_set.add(self.object)
		return response

	def get_success_url(self):
		return reverse_lazy('usuario:usuario_lista')



class ActualizarUsuario(PermissionRequiredMixin, UpdateView):
	model = User
	template_name = 'usuario/usuario_registrar.html'
	form_class = FormularioRegistro
	permission_required = 'auth.change_user'
	success_url = reverse_lazy('usuario:usuario_lista')

class EliminarUsuario(PermissionRequiredMixin, DeleteView):
	model = User
	template_name = 'usuario/usuario_eliminar.html'
	permission_required = 'auth.delete_user'
	success_url = reverse_lazy('usuario:usuario_lista')