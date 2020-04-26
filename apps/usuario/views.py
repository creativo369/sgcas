from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from apps.usuario.forms import UserForm
from django.urls import reverse_lazy
from SGCAS.decorators import administrator_only
from django.contrib.auth.models import User


# Create your views here.
@login_required
def usuario_view(request):
    """
    Permite visualizar la plantilla de bienvenida al sistema.
    :param request: Recibe un request por parte de un usuario.
    :return: Renderiza la plantilla usuario_home.html que es el home del sistema
    """
    return render(request, 'usuario/usuario_home.html')


@login_required
@administrator_only
def usuario_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un objeto de tipo User.
    :param request:Recibe un request por parte un usuario (Administrador u otro usuario con los permisos).
    :return:Renderiza la plantilla usuario_opciones.html que contiene las opciones que se pueden realizar sobre un usuario.
    """
    return render(request, 'usuario/usuario_opciones.html')


class UsuarioLista(PermissionRequiredMixin, ListView):
    """
    Permite visualizar la lista de modelos de tipo User activos en el sistema.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: La vista a la plantilla usuario_lista.html con la lista de los usuarios activos en el sistema.
    """
    model = User
    template_name = 'usuario/usuario_lista.html'
    permission_required = 'auth.change_user'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']


class RegistrarUsuario(PermissionRequiredMixin, CreateView):
    """
    Permite crear instancias del modelo User  en el sistema de forma manual, sin allauth.
    :param PermissionRequiredMixin:Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param CreateView:Recibe una vista generica de tipo CreateView para vistas basadas en clases.
    :return: Una instancia de usuario que es almacenado en la base de datos.
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'auth.add_user'

    def for_valid(self, form):
        response = super(RegistrarUsuario, self).form_valid(form)
        username = form.cleaned_data['username']
        rol = form.cleaned_data['groups']
        g = Group.objects.get(name=rol)
        g.user_set.add(self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('usuario:usuario_lista')


class ActualizarUsuario(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('usuario:usuario_lista')


class EliminarUsuario(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param DeleteView:Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return:Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.
    """
    model = User
    template_name = 'usuario/usuario_eliminar.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('usuario:usuario_lista')
