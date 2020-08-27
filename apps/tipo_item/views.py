# === Importación de las librerias utilizadas de Django ===
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from guardian.mixins import PermissionRequiredMixin
from apps.tipo_item.forms import TipoItemForm, TipoItemUpdateForm

from django.db.models import Q
from django.core.paginator import Paginator
from apps.tipo_item.models import TipoItem
from apps.fase.models import Fase
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy

"""
Todas las vistas para la aplicación del Modulo Tipo de Ítem
Actualmente se despliega en las plantillas 6 vistas:

1. **crear_tipo_item** - definición de una instancia del modelo TipoItem (Ir a la sección: [[views.py #crear tipo de ítem]] )
2. **tipo_item_opciones** - despliega opciones (Ir a la sección: [[views.py #gestión tipo de ítem]] )
3. **tipo_item_lista** - lista los tipos de ítems del sistema (Ir a la sección: [[views.py #lista tipo de ítem]] )
4. **search** - lista los tipos de ítems buscados del sistema (Ir a la sección: [[views.py #search]] )
5. **eliminar_tipo_item** - elimina un tipo de ítem (Ir a la sección: [[views.py #eliminar tipo de ítem]] )
6. **editar_tipo_item** - modifica los atributos de un tipo de ítem (Ir a la sección: [[views.py #tipo de ítem update]] )
"""


@login_required
@permission_required('tipo_item.crear_tipo_item', raise_exception=True)
# === crear tipo de ítem ===
def crear_tipo_item(request, id_fase):
    """
    Permite la creacion de instancias de modelo TipoItem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
    **:param id_fase:** Recibe el id de la fase en la que se creará el tipo de ítem.<br/>
    **:return:**  Retorna una instancia del modelo TipoItem.<br/>
    """
    if request.method == 'POST':
        form = TipoItemForm(request.POST)
        if form.is_valid():
            ti = form.save(commit=False)
            ti.fase = get_object_or_404(Fase, pk=id_fase)
            ti.save()
        return redirect('tipo_item:tipo_item_lista', id_fase=id_fase)
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


@permission_required('tipo_item.listar_tipo_item', raise_exception=True)
# === lista tipo de ítem ===
def tipo_item_lista(request, id_fase):
    """
     Permite la visualizacion en lista de todas las intancias del modelo TipoItem.<br/>
    **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la fase a la que pertenece el tipo de ítem para listarlo.<br/>
     **:return:** Una vista de todas las intancias de tipo de ítem que se encuentra en la fase.<br/>
     """
    tipo_item = TipoItem.objects.filter(fase=get_object_or_404(Fase, pk=id_fase)).order_by('id').distinct()
    paginator = Paginator(tipo_item, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tipo_item/tipo_item_lista.html', {'fase': Fase.objects.get(id=id_fase),
                                                            'page_obj': page_obj})


@permission_required('tipo_item.editar_tipo_item', raise_exception=True)
# === tipo de ítem update ===
def editar_tipo_item(request, pk):
    """
     Permite la modificacion de informacion de una instancia de modelo TipoItem.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la fase a la que pertenece el tipo de ítem para modificarlo.<br/>
     **:return:** Modifica una instancia del modelo TipoItem, luego se redirige a la lista de tipo de ítems.<br/>
    """
    ti = get_object_or_404(TipoItem, pk=pk)
    form = TipoItemUpdateForm(request.POST or None, instance=ti)
    if form.is_valid():
        form.save()
        return redirect('tipo_item:tipo_item_lista', id_fase=ti.fase.pk)
    return render(request, 'tipo_item/tipo_item_modificar.html', {'form':form})


@permission_required('tipo_item.eliminar_tipo_item', raise_exception=True)
# === eliminar tipo de ítem ===
def eliminar_tipo_item(request, pk):
    """
     Permite la visualizacion en lista de todas las intancias del modelo TipoItem que se encuentran en una fase.<br/>
     **:param request:** Recibe un request por parte de un usuario.<br/>
     **:param pk:** Recibe el pk de la fase a la que pertenece el tipo de ítem para eliminarlo.<br/>
     **:return:** Una vista de todas las intancias  de TipoItem existentes en la fase.<br/>
    """
    ti = get_object_or_404(TipoItem, pk=pk)
    id_fase = ti.fase.pk
    ti.delete()
    return redirect('tipo_item:tipo_item_lista', id_fase=id_fase)

        
@permission_required('tipo_item.listar_tipo_item', raise_exception=True)
# === search === 
def search(request, id_fase):
    """
    Permite realizar la búsqueda de las intancias del modelo TipoItem.<br/>
    *:param request:** Recibe un request por parte un usuario.<br/> 
    **:param id_fase:** Recibe el id de la instancia de fase, de la cual requerimos la lista de tipos de ítem.<br/>  
    **:return:** retorna una lista con todos los Tipos de Ítem  de que cumplen con los criterios de búsqueda.<br/>
    """
    template = 'tipo_item/list_busqueda.html'
    query = request.GET.get('buscar')

    if query:
        results = TipoItem.objects.filter(Q(fase=get_object_or_404(Fase, pk=id_fase)) 
            & Q(nombre__icontains=query) | Q(descripcion__contains=query)).order_by('id').distinct()
    else:
        results= TipoItem.objects.filter(Q(fase=get_object_or_404(Fase, pk=id_fase))).order_by('id').distinct()
   
    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)     
    
    return render(request, template, {'fase': Fase.objects.get(id=id_fase),'page_obj': page_obj})



# === Índice de la documentación de la Aplicación Comité  === <br/>
# 1.apps    : [[apps.py]]<br/>
# 2.forms   : [[forms.py]]<br/>
# 3.models  : [[models.py]]<br/>
# 4.tests   : [[tests.py]]<br/>
# 5.urls    : [[urls.py]]<br/>
# 6.views   : [[views.py]]<br/>
