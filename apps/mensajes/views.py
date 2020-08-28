# === Importación de las librerias utilizadas de Django ===
from apps.usuario.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.usuario.forms import FormularioUsuarioActivar

"""
Todas las vistas para la aplicación del Modulo Mensaje
Actualmente se despliega en las plantillas 3 vistas:

1. **Mensajes** - lista los usuarios cuya entrada al sistema debe ser aprobada (Ir a la sección: [[views.py #mensajes]] )
2. **Actualizar Usuario** - modifica la información correspondiente a cada usuario (Ir a la sección: [[views.py #actualizacion usuario]] )
3. **Eliminar Usuario** - quita  del sistema a un determinado usuario (Ir a la sección: [[views.py #eliminar usuario]] )

"""

# === mensajes ===
class Mensajes(ListView):
    """
    Permite la visualizacion de instancias del modelo User con estado inactivo<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Renderiza la plantilla mensaje_lista.html con las instancias del modelo User de estado inactivo.<br/>
    """

    paginate_by = 4
    model = User
    template_name = 'mensajes/mensajes_lista.html'
    permission_required = 'usuario.ver_mensaje'

    def get_queryset(self):
        #ordena la lista de usuarios excluyendo al AnonymousUser
        return User.objects.filter(is_active=False).order_by('id').distinct().exclude(username='AnonymousUser')


# === actualizacion usuario ===
class ActualizarUsuarioMensaje(PermissionRequiredMixin, UpdateView):
    """
    Permite la actualizacion de informacion de una instancia de modelo User.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Una instancia actualizada del modelo User, luego se redirige a la lista de usuarios.<br/>
    """
    model = User
    template_name = 'mensajes/mensaje_editar.html'
    form_class = FormularioUsuarioActivar
    permission_required = 'usuario.mensaje_editar'
    success_url = reverse_lazy('mensajes:mensaje_lista')


# === eliminar usuario ===
class EliminarUsuarioMensaje(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo User inactivo.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo User referenciado y se regresa a la lista de usuarios activos del sistema.<br/>
     """
    model = User
    template_name = 'mensajes/mensajes_eliminar.html'
    permission_required = 'usuario.mensaje_eliminar'
    success_url = reverse_lazy('mensajes:mensaje_lista')

# **Volver atras** :[[urls.py]]

# === Indice de la documentación de la Aplicación mensajes  === <br/>
# 1.apps                : [[apps.py]]<br/>
# 2.context_processors  : [[context_processors.py]]<br/>
# 3.test                : [[tests.py]]<br/>
# 4.urls                : [[urls.py]]<br/>
# 5.views               : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)