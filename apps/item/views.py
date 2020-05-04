from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from guardian.mixins import PermissionRequiredMixin

from apps.fase.models import Fase
from apps.item.forms import ItemForm, ItemUpdateForm, ItemImportarTipoItemForm, ItemAtributosForm, ItemCambiarEstado
from apps.item.models import Item
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
import pyrebase
from datetime import date

from apps.tipo_item.models import TipoItem

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
storage = firebase.storage()


def crear_item_basico(request, id_fase):
    """
    Permite la creacion de instancias de modelo Item.
    :param request: Recibe un request por parte de un usuario.
    :return:  Retorna una instancia del modelo Item.
    """
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, id_fase=id_fase)
        if form.is_valid():
            item = form.save(commit=False)
            item.fase = Fase.objects.get(id=id_fase)
            item.save()
            form.save_m2m()

            if request.FILES:
                ##ALMACENAMIENTO FIREBASE
                path_local = 'media/' + item.archivo.name  # Busca los archivos en MEDIA/NOMBREARCHIVO
                path_on_cloud = str(
                    date.today()) + '/' + item.archivo.name  # Se almacena en Firebase como FECHADEHOY/NOMBREARCHIVO
                storage.child(path_on_cloud).put(path_local)  # Almacena el archivo en Firebase
                ##

            return redirect('item:importar_tipo_item', pk=item.pk)
    else:
        form = ItemForm(id_fase=id_fase)

    return render(request, 'item/item_crear.html', {'form': form, 'tipo_item': TipoItem.objects.exists()})


def item_importar_ti(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemImportarTipoItemForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save()
        return redirect('item:set_atributos', pk=item.id)
    return render(request, 'item/item_importar_tipo_item.html', {'form': form,
                                                                 'tipo_item': TipoItem.objects.all().exists(),
                                                                 'fase': item.fase})


def item_set_atributos(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemAtributosForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=Item.objects.get(id=pk).fase.pk)
    return render(request, 'item/item_atributos_tipo_item.html', {'form': form,
                                                                  'fase': item.fase})


@login_required
def item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Item.
    :param request:Recibe un request por parte de un usuario.
    :return: Renderiza la plantilla usuario_home.html que es el home del sistema
    """

    return render(request, 'item/item_opciones.html')


def item_lista_fase(request, id_fase):
    return render(request, 'item/item_lista.html', {'items': Item.objects.filter(fase=Fase.objects.get(id=id_fase)),
                                                    'proyecto': Fase.objects.get(id=id_fase).proyecto})


def item_eliminar(request, pk):
    item = Item.objects.get(id=pk)
    id_fase = item.fase.pk
    item.delete()
    return redirect('item:item_lista', id_fase=id_fase)


def item_modificar_basico(request, pk):
    item = get_object_or_404(Item, pk=pk)
    id_fase = item.fase.pk
    form = ItemUpdateForm(request.POST or None, instance=item, id_fase=id_fase)
    if form.is_valid():
        item = form.save()
        return redirect('item:item_modificar_import_ti', pk=item.pk)
    return render(request, 'item/item_crear.html', {'form': form, 'tipo_item': TipoItem.objects.exists()})


def item_modificar_ti(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemImportarTipoItemForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save()
        return redirect('item:item_modificar_atr_ti', pk=item.pk)
    return render(request, 'item/item_importar_tipo_item.html', {'form': form, 'fase': item.fase, 'item': item})


def item_modificar_atributos(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemAtributosForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=item.fase.pk)
    return render(request, 'item/item_atributos_tipo_item.html', {'form': form})


def item_cambiar_estado(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemCambiarEstado(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item:item_lista', id_fase=item.fase.pk)
    return render(request, 'item/item_cambiar_estado.html', {'form': form, 'item': item})


class ItemLista(ListView, PermissionRequiredMixin, LoginRequiredMixin):
    """
    Permite la visualizacion en lista de todas las intancias del modelo Item
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :param ListView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :return: Una vista de todas las intancias a traves del archivo item_lista.html.
    """
    model = Item
    template_name = 'item/item_lista.html'
    permission_required = 'item.view_item'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']


class ItemEliminar(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):
    """
    Permite la eliminacion instancias de modelos Item.
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :param DeleteView: Recibe una vista generica de tipo DeleteView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :return: Elimina una instancia del modelo Item del sistema.
    """
    model = Item
    template_name = 'item/item_eliminar.html'
    permission_required = 'item.delete_item'
    success_url = reverse_lazy('item:item_lista')


class ItemModificar(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    """
    Permite la modificacion de informacion basica de una instancia de modelo Item.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :return: Modficia una instancia del modelo Item, luego se redirige para la importacion de Tipo de Item.
    """
    model = Item
    template_name = 'item/item_crear.html'
    form_class = ItemUpdateForm
    permission_required = 'item.change_item'

    def form_valid(self, form):
        object = form.save()
        return redirect('item:item_modificar_import_ti', pk=object.pk)


class ItemModificarImportTI(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    """
    Permite la modificacion de importacion de Tipo de Item de una instancia de modelo Item.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :return: Modifica una instancia del modelo Item, luego se redirige para setear los atrobutos del Tipo de Item importado
    """
    model = Item
    template_name = 'item/item_importar_tipo_item.html'
    form_class = ItemImportarTipoItemForm
    permission_required = 'item.change_item'

    def form_valid(self, form):
        object = form.save()
        return redirect('item:item_modificar_atr_ti', pk=object.pk)


class ItemModificarAtrTI(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    """
    Permite la modificacion de atributos de una instancia de modelo Item.
    :param PermissionRequiredMixin: Maneja multiple permisos, de la libreria guardian.mixins.
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :return: Modifica na instancia del modelo Item, luego se redirige a la lista de items.
    """
    model = Item
    template_name = 'item/item_atributos_tipo_item.html'
    form_class = ItemAtributosForm
    permission_required = 'item.change_item'
    success_url = reverse_lazy('item:item_lista')

# **Atras** : [[urls.py]]

# === Indice de la documentación de la Aplicación item  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
