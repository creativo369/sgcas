# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from guardian.decorators import permission_required
from guardian.mixins import PermissionRequiredMixin
from apps.tipo_item.forms import TipoItemForm, TipoItemUpdateForm
from apps.tipo_item.models import TipoItem
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy

"""
Todas las vistas para la aplicación del Modulo Comité
Actualmente se despliega en las plantillas 5 vistas:


1. **crear tipo de item** - definición de una instancia del modelo comité (Ir a la sección: [[views.py#creartipo]] )
2. **Gestión de tipo de item** - modificar una instancia del modelo comité (Ir a la sección: [[views.py#gestiontipo]] )
3. **Listar tipo de items ** - suprimir una instancia del modelo comité (Ir a la sección: [[views.py#listaitem]] )
4. **Tipo de item eliminar ** - ver detalles de una instancia del modelo comité (Ir a la sección: [[views.py#eliminartipo]] )
5. **Tipo de Item modificar** - operación exitosa para la creación de un comite (Ir a la sección: [[views.py#tipoiteupdate]] )
"""


@login_required
@permission_required('tipo_item.add_tipo_item')
# === creartipo ===
def crear_tipo_item(request):
    """
    Permite la creacion de instancias de modelo TipoItem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:**  Retorna una instancia del modelo TipoItem.<br/>
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
# === gestiontipo ===
def tipo_item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo TipoItem.
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema<br/>
    """

    return render(request, 'tipo_item/tipo_item_opciones.html')


# === listaitem ===
class TipoItemLista(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion en lista de todas las intancias del modelo TipoItem<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Una vista de todas las intancias a traves del archivo tipo_item_lista.html.<br/>
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_lista.html'
    permission_required = 'tipo_item.view_tipo_item'

    # La lista a mostrar estara por orden ascendente
    class Meta:
        ordering = ['-id']


# === eliminartipo ===
class TipoItemEliminar(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminacion instancias de modelos TipoItem.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Elimina una instancia del modelo TipoItem del sistema.<br/>
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_eliminar.html'
    permission_required = 'tipo_item.delete_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')


# === tipoiteupdate ===
class TipoItemModificar(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de informacion de una instancia de modelo TipoItem.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria guardian.mixins.<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Modficia na instancia del modelo TipoItem, luego se redirige a la lista de tipo de items.<br/>
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_modificar.html'
    form_class = TipoItemUpdateForm
    permission_required = 'tipo_item.change_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
