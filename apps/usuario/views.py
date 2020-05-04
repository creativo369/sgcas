# === Importación de las librerias utilizadas de Django ===
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from apps.usuario.forms import UserForm
from django.urls import reverse_lazy
from SGCAS.decorators import administrator_only
"""
Todas las vistas para la aplicación del Modulo Usuario
Actualmente se despliega en las plantillas 5 vistas:

1. **usuario_view** -  Un lobby para los usuarios del sistema (Ir a la sección: [[views.py#usuarioview]] )
2. **Gestión Usuarios** -  Despliega la gestión de usuarios (Ir a la sección: [[views.py#gestionusuarios]] )
3. **Listado Usuario** -  Despliega el listado de los usuarios (Ir a la sección: [[views.py#usuariolistado]] )
4. **Registrar Usuario ** -  Despliega el registro para nuevos usuarios (Ir a la sección: [[views.py#registrousuario]] )
5. **Actualizar Usuario ** - Despliega la actualización de usuarios (Ir a la sección: [[views.py#actualizarusuario]] )
5. **Eliminar Usuario ** - Despliega la eliminación de usuarios (Ir a la sección: [[views.py#eliminarusuario]] )
"""

@login_required
# === usuarioview ===
def usuario_view(request):
    """
    Una vista de lobby para los usuarios registrados en el sistema. <br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema<br/>
    """
    return render(request, 'usuario/usuario_home.html')


@login_required
@administrator_only
# === gestionusuarios ===
def usuario_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un objeto de tipo User.
    **:param request:** Recibe un request por parte un usuario (Administrador u otro usuario con los permisos).<br/>
    **:return:** Renderiza la plantilla usuario_opciones.html que contiene las opciones que se pueden realizar sobre un usuario.<br/>
    """
    return render(request, 'usuario/usuario_opciones.html')

# === usuariolistado ===
class UsuarioLista(PermissionRequiredMixin, ListView):
    """
    Permite visualizar la lista de modelos de tipo User activos en el sistema.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** La vista a la plantilla usuario_lista.html con la lista de los usuarios activos en el sistema.<br/>
    """
    model = User
    template_name = 'usuario/usuario_lista.html'
    permission_required = 'auth.change_user'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']

# === registrousuario ===
class RegistrarUsuario(PermissionRequiredMixin, CreateView):
    """
    Permite crear instancias del modelo User  en el sistema de forma manual, sin allauth.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param CreateView:** Recibe una vista generica de tipo CreateView para vistas basadas en clases.<br/>
    **:return:** Una instancia de usuario que es almacenado en la base de datos.<br/>
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'usuario.crear_usuario'

    def for_valid(self, form):
        response = super(RegistrarUsuario, self).form_valid(form)
        username = form.cleaned_data['username']
        rol = form.cleaned_data['groups']
        g = Group.objects.get(name=rol)
        g.user_set.add(self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('usuario:usuario_lista')

# === actualizarusuario ===
class ActualizarUsuario(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.<br/>
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.<br/>
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'usuario.editar_usuario'
    success_url = reverse_lazy('usuario:usuario_lista')

# === eliminarusuario ===
class EliminarUsuario(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.<br/>
    """
    model = User
    template_name = 'usuario/usuario_eliminar.html'
    permission_required = 'usuario.eliminar_usuario'
    success_url = reverse_lazy('usuario:usuario_lista')

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>
