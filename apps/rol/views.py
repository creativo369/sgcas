# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rol.forms import GroupForm
from django.shortcuts import render, redirect
"""
Todas las vistas para la aplicación del Modulo Rol
Actualmente se despliega en las plantillas 5 vistas:

1. **crear rol ** - funcion para la creación de roles  (Ir a la sección: [[views.py#crearrol]] )
2. **gestion de roles ** - vista que despliega la gestión de roles (Ir a la sección: [[views.py#rolopciones]] )
3. **Listar roles ** - Lista los roles existentes (Ir a la sección: [[views.py#listaroles]] )
4. **Editar un rol  ** - se puede editar un rol (Ir a la sección: [[views.py#editarrol]] )
5. **Eliminar un rol ** - se puede eliminar un rol (Ir a la sección: [[views.py#eliminarrol]] )
"""
@login_required
@permission_required('auth.add_group')
# === crearrol ===
def crear_rol_view(request):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Group.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Se almacena una instancia del modelo Group.<br/>
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('rol:rol_lista')
    else:
        form = GroupForm()
    return render(request, 'rol/rol_crear.html', {'form': form})


@login_required
@permission_required('auth.view_group')
# === rolopciones ===
def rol_opciones(request):
    """
    Permite la visualizacion de las opciones sobre el modelo Group.<br/>
    **:param request:** Recibe un request por parte un usuario.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    return render(request, 'rol/rol_opciones.html')

# === listaroles ===
class ListaRol(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion de todas las intancias del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Lista que contiene todas las instancias del modelo Group del sistema.<br/>
    """
    model = Group
    template_name = 'rol/rol_lista.html'
    permission_required = 'auth.change_group'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']

# === editarrol ===
class EditarRol(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de una instancia del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Se modifica la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Group
    form_class = GroupForm
    permission_required = 'auth.change_group'
    template_name = 'rol/rol_editar.html'
    success_url = reverse_lazy('rol:rol_lista')

# === eliminarrol ===
class EliminarRol(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo Group.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria django.contrib.auth.mixins.<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Se elimina la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.<br/>
    """
    model = Group
    template_name = 'rol/rol_eliminar.html'
    permission_required = 'auth.delete_group'
    success_url = reverse_lazy('rol:rol_lista')


# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>