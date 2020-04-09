from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from SGCAS.decorators import administrator_only
from apps.usuario.forms import UserForm

class Mensajes(ListView):
    """
    Permite la visualizacion de instancias del modelo User con estado inactivo
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Renderiza la plantilla mensaje_lista.html con las instancias del modelo User de estado inactivo.
    """
    model = User
    template_name = 'mensajes/mensajes_lista.html'


class ActualizarUsuarioMensaje(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.
    """
    model = User
    template_name = 'mensajes/mensaje_editar.html'
    form_class = UserForm
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('mensajes:mensaje_lista')


class EliminarUsuarioMensaje(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User inactivo.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins
    :param DeleteView:Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return:Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.
     """
    model = User
    template_name = 'mensajes/mensajes_eliminar.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('mensajes:mensaje_lista')
