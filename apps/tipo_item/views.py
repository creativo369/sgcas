from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from guardian.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin
from apps.tipo_item.forms import TipoItemForm, TipoItemUpdateForm
from apps.tipo_item.models import TipoItem
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from apps.tipo_item.models import ATTRIBUTES


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
        return redirect('tipo_item:tipo_item_lista')
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
    template_name = 'tipo_item/tipo_item_modificar.html'
    form_class = TipoItemUpdateForm
    permission_required = 'tipo_item.change_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')


def func(request, id):
    object = TipoItem.objects.get(id=id)
    nombre = object.nombre
    descripcion = object.descripcion

    str_attr = object.atributos
    str_attr = str(str_attr)
    str_attr = str_attr.split(',')
    print(str_attr)
    print(str_attr[0])
    print(type(str_attr[1]))

    print(str_attr[0] == 'Char')

    form = TipoItemForm(instance=object)

    return render(request, 'tipo_item/tipo_item_modificar.html', {'form': form})
