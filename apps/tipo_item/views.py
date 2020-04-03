from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from guardian.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin
from apps.tipo_item.forms import TipoItemForm
from apps.tipo_item.models import TipoItem
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy


@login_required
@permission_required('tipo_item.add_tipo_item')
def crear_tipo_item(request):
    """
    Permite la creacion de instancias de modelo TipoItem.
    :param request: Recibe un request por parte de un usuario.
    :return:  Retorna una instancia del modelo TipoItem.
    """
    if request.method == 'POST':
        form = TipoItemForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('tipo_item:tipo_item_opciones')
    else:
        form = TipoItemForm()

    return render(request, 'tipo_item/tipo_item_crear.html', {'form': form})


@login_required
@permission_required('tipo_item.view_tipo_item')
def tipo_item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo TipoItem.
    :param request:Recibe un request por parte de un usuario.
    :return: Renderiza la plantilla usuario_home.html que es el home del sistema
    """

    return render(request, 'tipo_item/tipo_item_opciones.html')


class TipoItemLista(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion en lista de todas las intancias del modelo TipoItem
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :return: Una vista de todas las intancias a traves del archivo tipo_item_lista.html.
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_lista.html'
    permission_required = 'tipo_item.view_tipo_item'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']


class TipoItemEliminar(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion instancias de modelos TipoItem.
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :return: Elimina una instancia del modelo TipoItem del sistema.
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_eliminar.html'
    permission_required = 'tipo_item.delete_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')

class TipoItemModificar(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de informacion de una instancia de modelo TipoItem.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :return: Modficia na instancia del modelo TipoItem, luego se redirige a la lista de tipo de items.
    """
    model = TipoItem
    template_name = 'usuario/usuario_registrar.html'
    form_class = TipoItemForm
    permission_required = 'tipo_item.change_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')
