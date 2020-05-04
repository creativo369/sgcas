# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.usuario.forms import UserForm

"""
Todas las vistas para la aplicación del Modulo Mensaje
Actualmente se despliega en las plantillas 5 vistas:

1. **Mensajes** - operación exitosa para la creación de un comite (Ir a la sección: [[views.py#mensajes]] )
2. **Actualizar Usuario** - definición de una instancia del modelo comité (Ir a la sección: [[views.py#actualizacionusuario]] )
3. **Eliminar Usuario** - modificar una instancia del modelo comité (Ir a la sección: [[views.py#eliminarusuario]] )

"""


# === mensajes ===
class Mensajes(ListView):
    """
    Permite la visualizacion de instancias del modelo User con estado inactivo<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Renderiza la plantilla mensaje_lista.html con las instancias del modelo User de estado inactivo.<br/>
    """
    model = User
    template_name = 'mensajes/mensajes_lista.html'


# === actualizacionusuario ===
class ActualizarUsuarioMensaje(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.<br/>
    """
    model = User
    template_name = 'mensajes/mensaje_editar.html'
    form_class = UserForm
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('mensajes:mensaje_lista')


# === eliminarusuario ===
class EliminarUsuarioMensaje(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User inactivo.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.<br/>
     """
    model = User
    template_name = 'mensajes/mensajes_eliminar.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('mensajes:mensaje_lista')

# **Volver atras** :[[urls.py]]

# === Indice de la documentación de la Aplicación mensajes  === <br/>
# 1.apps                : [[apps.py]]<br/>
# 2.context_processors  : [[context_processors.py]]<br/>
# 3.test                : [[tests.py]]<br/>
# 4.urls                : [[urls.py]]<br/>
# 5.views               : [[views.py]]<br/>
