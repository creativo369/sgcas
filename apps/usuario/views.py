# === Importación de las librerias utilizadas de Django ===
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group

from django.db.models import Q
from django.core.paginator import Paginator
from apps.usuario.forms import UserForm
from django.urls import reverse_lazy
from SGCAS.decorators import administrator_only
from apps.usuario.models import User

"""
Todas las vistas para la aplicación del Modulo Usuario
Actualmente se despliega en las plantillas 7 vistas:

1. **usuario_view** - despliega la página principal del sistema para el usuario (Ir a la sección: [[views.py #usuarioview]] )
2. **usuario_opciones** - despliega opciones (Ir a la sección: [[views.py #gestion usuarios]] )
3. **UsuarioLista** - despliega el listado de los usuarios (Ir a la sección: [[views.py #usuarios listados]] )
4. **search** - despliega el listado de los usuarios  buscados en el sistema (Ir a la sección: [[views.py #search]] )
5. **RegistrarUsuario** - registra los nuevos usuarios en el sistema (Ir a la sección: [[views.py #registro usuarios]] )
6. **ActualizarUsuario** - actualiza los datos de los usuarios (Ir a la sección: [[views.py #actualizar usuario]] )
7. **EliminarUsuario** - elimina usuarios del sistema (Ir a la sección: [[views.py #eliminar usuario]] )
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
# === gestion usuarios ===
def usuario_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un objeto de tipo User.
    **:param request:** Recibe un request por parte un usuario (Administrador u otro usuario con los permisos).<br/>
    **:return:** Renderiza la plantilla usuario_opciones.html que contiene las opciones que se pueden realizar sobre un usuario.<br/>
    """
    return render(request, 'usuario/usuario_opciones.html')


# === usuarios listados ===
class UsuarioLista(PermissionRequiredMixin, ListView):
    """
    Permite visualizar la lista de modelos de tipo User activos en el sistema.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** La vista a la plantilla usuario_lista.html con la lista de los usuarios activos en el sistema.<br/>
    """

    paginate_by = 4
    model = User
    template_name = 'usuario/usuario_lista.html'
    permission_required = 'usuario.ver_usuario'

    def get_queryset(self):
        # se ordena la lista de usuarios, excluyendo al AnonymousUser.
        return User.objects.order_by('id').distinct().exclude(username='AnonymousUser').exclude(is_superuser=True)


@permission_required('usuario.ver_usuarios', raise_exception=True)
# === search ===
def search(request):
    """
    Permite realizar la búsqueda de los usuarios  activos en el sistema.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** retorna una lista con los usuarios que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'usuario/list_busqueda.html'
    query = request.GET.get('buscar')

    if query:
        results = User.objects.filter(Q(username__icontains=query) |
                                      Q(first_name__icontains=query)).order_by('id').distinct().exclude(
            username='AnonymousUser')
    else:
        results = User.objects.all().order_by('id').exclude(username='AnonymousUser')

    paginator = Paginator(results, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'page_obj': page_obj})


# === registro usuarios ===
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
    permission_required = 'usuario.registrar_usuario'

    def for_valid(self, form):
        response = super(RegistrarUsuario, self).form_valid(form)
        username = form.cleaned_data['username']
        rol = form.cleaned_data['groups']
        g = Group.objects.get(name=rol)
        g.user_set.add(self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('usuario:usuario_lista')


# === actualizar usuario ===
class ActualizarUsuario(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualización de información de una instancia de modelo User.<br/>
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.<br/>
    """
    model = User
    template_name = 'usuario/usuario_registrar.html'
    form_class = UserForm
    permission_required = 'usuario.editar_usuario'
    success_url = reverse_lazy('usuario:usuario_lista')


# === eliminar usuario ===
class EliminarUsuario(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminación de una instancia del modelo User.<br/>
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

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)
