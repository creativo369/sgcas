from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from guardian.mixins import PermissionRequiredMixin
from apps.item.forms import ItemForm, ItemUpdateForm, ItemImportarTipoItemForm, ItemAtributosForm
from apps.item.models import Item
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy

# Configuracion para el Firebase
firebase_config = {
    "apiKey": "AIzaSyBOoFqZqkV7SpkMMN_ZXqm7SXBRW08dMus",
    "authDomain": "sgcas-f6ab6.firebaseapp.com",
    "databaseURL": "https://sgcas-f6ab6.firebaseio.com",
    "projectId": "sgcas-f6ab6",
    "storageBucket": "sgcas-f6ab6.appspot.com",
    "messagingSenderId": "206850965617",
    "appId": "1:206850965617:web:7b6265bb6e26e6a9ccdbd0"
}


class ItemCrear(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la creacion de una instancia de un objeto Item
    :param CreateView: Recibe una vista generica de tipo ListView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :return: Una instancia de objeto Item.
    """
    model = Item
    form_class = ItemForm
    permission_required = 'item.add_item'
    template_name = 'item/item_crear.html'

    def form_valid(self, form):
        object = form.save()
        return redirect('item:importar_tipo_item', pk=object.pk)


class ImportarTipoItem(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite la importacion de una instancia de un objeto Tipo de Item a una instancia de objeto Item
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :return: Una instancia de Item enlazado con una instancia de Tipo de Item.
    """
    model = Item
    form_class = ItemImportarTipoItemForm
    permission_required = 'item.change_item'
    template_name = 'item/item_importar_tipo_item.html'

    def form_valid(self, form):
        object = form.save()
        return redirect('item:set_atributos', pk=object.pk)


class SetAtributos(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Permite agregar los atributos de Tipo de Item a una instancia de Item al que fue relacionado.
    :param UpdateView: Recibe una vista generica de tipo UpdateView para vistas basadas en clases.
    :param LoginRequiredMixin: Acceso controlado por logueo, de la libreria auth.mixins.
    :param PermissionRequiredMixin: Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.
    :return: Una instancia de objeto Item, relacionado con su Tipo de Item y sus atributos seteados.
    """
    model = Item
    form_class = ItemAtributosForm
    permission_required = 'item.change_item'
    template_name = 'item/item_atributos_tipo_item.html'
    success_url = reverse_lazy('item:item_lista')


@login_required
def item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo Item.
    :param request:Recibe un request por parte de un usuario.
    :return: Renderiza la plantilla usuario_home.html que es el home del sistema
    """

    return render(request, 'item/item_opciones.html')


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
