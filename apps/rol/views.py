from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.rol.forms import GroupForm
from django.shortcuts import render, redirect

@login_required
@permission_required('auth.add_group')
def crear_rol_view(request):
    """
    Permite la visualizacion de la plantilla para la creacion de instancias del modelo Group.
    :param request: Recibe un request por parte de un usuario.
    :return: Se almacena una instancia del modelo Group.
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
def rol_opciones(request):
    """
    Permite la visualizacion de las opciones sobre el modelo Group.
    :param request: Recibe un request por parte un usuario.
    :return: Lista que contiene todas las instancias del modelo Group del sistema.
    """
    return render(request, 'rol/rol_opciones.html')


class ListaRol(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion de todas las intancias del modelo Group.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins.
    :param ListView:Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Lista que contiene todas las instancias del modelo Group del sistema.
    """
    model = Group
    template_name = 'rol/rol_lista.html'
    permission_required = 'auth.change_group'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']


class EditarRol(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de una instancia del modelo Group.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins.
    :param UpdateView:Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return:Se modifica la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.
    """
    model = Group
    form_class = GroupForm
    permission_required = 'auth.change_group'
    template_name = 'rol/rol_editar.html'
    success_url = reverse_lazy('rol:rol_lista')


class EliminarRol(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion de una instancia del modelo Group.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria django.contrib.auth.mixins.
    :param DeleteView:Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return:Se elimina la instancia del modelo Group referenciado y se regresa a la lista de roles del sistema.
    """
    model = Group
    template_name = 'rol/rol_eliminar.html'
    permission_required = 'auth.delete_group'
    success_url = reverse_lazy('rol:rol_lista')
