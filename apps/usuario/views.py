"""
Las vistas para el modulo de usuario

***Actualmente admitimos los las siguientes vistas:***

1.**Plantilla de Bienvenida** - usuario_view la pagina de inicio de bienvenida al usuario al sistema.Ir al detalle de
la sección : [[views.py#usuario_view]]

2.**Opciones** - Visualiza la opciones de gestión de usuarios en el sistema.Ir al detalle de la sección
: [[views.py#usuario_opciones]]

3.**Lista de Usuarios** - Visualiza los detalles de los usuarios registrados y activos en el sistema.Ir al detalle de
 la sección : [[views.py#UsuarioLista]]

4.**Registrar Usuarios** - Vista que gestiona el registro de usuarios en el sistema.Ir al detalle de la sección :
 [[views.py#RegistrarUsuario]]

5.**Actualizar Usuarios** - Vista que gestiona la modificación de campos de formulario de un usuario.Ir al detalle de la sección :
 [[views.py#ActualizarUsuario]]

6.**Eliminar Usuario** - Vista que gestiona el borrado de usuarios del sistema. Ir al detalle de la sección :
 [[views.py#EliminarUsuario]]
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

# Definidos en [[usuario.forms.py]]
from apps.usuario.forms import UserForm
from SGCAS.decorators import administrator_only
# **Código fuente de las vistas**
@login_required
# === usuario_view ===
def usuario_view(request):
    """
    Permite visualizar la plantilla de bienvenida al sistema.

    **:param request:** Recibe un request por parte de un usuario.

    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema
    """
    return render(request, 'usuario/usuario_home.html')
@login_required
@administrator_only
# === usuario_opciones ===
def usuario_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un objeto de tipo User.

    **:param request:**Recibe un request por parte un usuario (Administrador u otro usuario con los permisos).

    **:return:**Renderiza la plantilla usuario_opciones.html que contiene las opciones que se pueden realizar sobre un usuario.
    """
    return render(request, 'usuario/usuario_opciones.html')
# === UsuarioLista ===
class UsuarioLista(PermissionRequiredMixin, ListView):
    """
    Permite visualizar la lista de modelos de tipo User activos en el sistema.

    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins

    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.

    **:return:** La vista a la plantilla usuario_lista.html con la lista de los usuarios activos en el sistema.
    """
    model = User
    template_name = 'usuario/usuario_lista.html'
    permission_required = 'auth.change_user'
    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']
# === RegistrarUsuario ===
class RegistrarUsuario(PermissionRequiredMixin, CreateView):
    """
    Permite crear instancias del modelo User  en el sistema de forma manual, sin allauth.

    **:param PermissionRequiredMixin:**Maneja multiple permisos, de la libreria django.contrib.auth.mixins

    **:param CreateView:**Recibe una vista generica de tipo CreateView para vistas basadas en clases.

    **:return:**Una instancia de usuario que es almacenado en la base de datos.
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
# === ActualizarUsuario ===
class ActualizarUsuario(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.

   **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins

   **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.

   **:return:** Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('usuario:usuario_lista')
# === EliminarUsuario ===
class EliminarUsuario(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User.

    **:param PermissionRequiredMixin:**Maneja multiple permisos, de la libreria django.contrib.auth.mixins

    **:param DeleteView:**Recibe una vista generica de tipo DeleteView para vistas basadas en clases.

    **:return:**Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.
    """
    model = User
    template_name = 'usuario/usuario_eliminar.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('usuario:usuario_lista')