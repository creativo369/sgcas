# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from guardian.mixins import PermissionRequiredMixin
from apps.tipo_item.forms import TipoItemForm, TipoItemUpdateForm

from django.db.models import Q
from django.core.paginator import Paginator
from apps.tipo_item.models import TipoItem
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy

"""
Todas las vistas para la aplicación del Modulo Tipo de Ítem
Actualmente se despliega en las plantillas 6 vistas:

1. **crear_tipo_item** - definición de una instancia del modelo TipoItem (Ir a la sección: [[views.py #crear tipo de ítem]] )
2. **tipo_item_opciones** - despliega opciones (Ir a la sección: [[views.py #gestión tipo de ítem]] )
3. **TipoItemLista** - lista los tipos de ítems del sistema (Ir a la sección: [[views.py #lista tipo de ítem]] )
4. **search** - lista los tipos de ítems buscados del sistema (Ir a la sección: [[views.py #search]] )
5. **TipoItemEliminar** - elimina un tipo de ítem (Ir a la sección: [[views.py #eliminar tipo de ítem]] )
6. **TipoItemModificar** - modifica los atributos de un tipo de ítem (Ir a la sección: [[views.py #tipo de ítem update]] )
"""


@login_required
@permission_required('tipo_item.crear_tipo_item', raise_exception=True)
# === crear tipo de ítem ===
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
@permission_required('tipo_item.ver_tipo_item', raise_exception=True)
# === gestión tipo de ítem ===
def tipo_item_opciones(request):
    """
    Permite visualizar la plantilla de opciones que se pueden realizar sobre un modelo TipoItem.
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:return:** Renderiza la plantilla usuario_home.html que es el home del sistema.<br/>
    """

    return render(request, 'tipo_item/tipo_item_opciones.html')


# === lista tipo de ítem ===
class TipoItemLista(PermissionRequiredMixin, ListView):
    """
    Permite la visualizacion en lista de todas las intancias del modelo TipoItem.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
    **:param ListView:** Recibe una vista generica de tipo ListView para vistas basadas en clases.<br/>
    **:return:** Una vista de todas las intancias a traves del archivo tipo_item_lista.html.<br/>
    """
    paginate_by = 4
    model = TipoItem
    template_name = 'tipo_item/tipo_item_lista.html'
    permission_required = 'tipo_item.listar_tipo_item'

    # La lista a mostrar estara por orden ascendente
    #class Meta:
        #ordering = ['-id']
    def get_queryset(self):
        #ordena la lista de tipos de ítems
        return TipoItem.objects.order_by('id').distinct()
        
@permission_required('tipo_item.listar_tipo_item', raise_exception=True)
# === search === 
def search(request):
    """
    Permite realizar la búsqueda de las intancias del modelo TipoItem.<br/>
    *:param request:** Recibe un request por parte un usuario.<br/>   
    **:return:** retorna una lista con todos los Tipos de Ítem que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'tipo_item/list_busqueda.html'
    query = request.GET.get('buscar')

    if query:
        results = TipoItem.objects.filter(Q(nombre__icontains=query) | Q(descripcion__contains=query)).order_by('id').distinct()
    else:
        results= TipoItem.objects.all().order_by('id')
   
    paginator = Paginator(results, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)     
    
    return render(request, template, {'page_obj': page_obj})

# === eliminar tipo de ítem ===
class TipoItemEliminar(PermissionRequiredMixin, DeleteView):
    """
    Permite la eliminación instancias de modelos TipoItem.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos sobre objetos, de la libreria guardian.mixins.<br/>
    **:param DeleteView:** Recibe una vista generica de tipo DeleteView para vistas basadas en clases.<br/>
    **:return:** Elimina una instancia del modelo TipoItem del sistema.<br/>
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_eliminar.html'
    permission_required = 'tipo_item.eliminar_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')


# === tipo de ítem update ===
class TipoItemModificar(PermissionRequiredMixin, UpdateView):
    """
    Permite la modificacion de informacion de una instancia de modelo TipoItem.<br/>
    **:param PermissionRequiredMixin:** Maneja multiple permisos, de la libreria guardian.mixins.<br/>
    **:param UpdateView:** Recibe una vista generica de tipo UpdateView para vistas basadas en clases.<br/>
    **:return:** Modifica una instancia del modelo TipoItem, luego se redirige a la lista de tipo de ítems.<br/>
    """
    model = TipoItem
    template_name = 'tipo_item/tipo_item_modificar.html'
    form_class = TipoItemUpdateForm
    permission_required = 'tipo_item.editar_tipo_item'
    success_url = reverse_lazy('tipo_item:tipo_item_lista')

# === Índice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
